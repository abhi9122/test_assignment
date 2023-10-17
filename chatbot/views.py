from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserLoginSerializer, UserSignupSerializer, ChatbotSerializer, QuestionsSerializer, MessageSerializer, IncomingMessageSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Chatbot, Questions, Message, ChatbotUser, Customer
from .chatbot import TwilioHelper
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from .model_helpers import MessageUserTypeChoice
from django.utils import timezone
from .chat_promt import ChatGPTClient
from django.http import Http404


class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_201_CREATED
        return response


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request=request,
                            username=email, password=password)
        user = ChatbotUser.objects.get(email=email)

        # create token for the user to access login auths
        if user:
            token, created = Token.objects.get_or_create(user=user.user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ChatbotCreateView(generics.CreateAPIView):
    serializer_class = ChatbotSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # create chatbot
        user = self.request.user
        chatbot_user = user.chatbot_user
        serializer.save(user=chatbot_user)


class ChatbotRetrieveView(generics.ListAPIView):
    serializer_class = ChatbotSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.chatbot_user
        print(Chatbot.objects.filter(user=user))
        return Chatbot.objects.filter(user=user)


class ChatbotUpdateView(generics.UpdateAPIView):
    serializer_class = ChatbotSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.chatbot_user
        return Chatbot.objects.filter(user=user)


class QuestionsCreateView(generics.CreateAPIView):
    serializer_class = QuestionsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chatbot_id = self.kwargs["chatbot_id"]

        try:
            chatbot = Chatbot.objects.get(id=str(chatbot_id))
        except Chatbot.DoesNotExist:
            # Handle the case where the chatbot does not exist
            # You can choose to raise an exception or return an error response
            return Response({'error': 'Invalid chatbot id'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer.save(chatbot=chatbot)


class QuestionsUpdateView(generics.UpdateAPIView):
    serializer_class = QuestionsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Questions.objects.all()

    def perform_update(self, serializer):
        q_id = self.kwargs["pk"]
        try:
            quest = Questions.objects.get(id=str(q_id))
        except Questions.DoesNotExist:
            raise Http404("Question does not exist")
        else:
            quest.question = serializer.validated_data['question']
            quest.answer = serializer.validated_data['answer']
            quest.save()  



class QuestionsListView(generics.ListAPIView):
    serializer_class = QuestionsSerializer

    def get_queryset(self):
        chatbot_id = self.kwargs['chatbot_id']
        return Questions.objects.filter(chatbot__id=str(chatbot_id))


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class MessageRetrieveView(generics.ListAPIView):
    queryset = Message.objects.all().order_by('-created')

    serializer_class = MessageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# Read message from Twillio webhook
class TwilioWebhookView(APIView):
    def post(self, request, *args, **kwargs):

        # get from request data
        chatbot_id = request.query_params.get('chatbot_id')
        creator_id = request.query_params.get('creator_id')

        try:
            chatbot = Chatbot.objects.get(id=chatbot_id)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid chatbot'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            creator = ChatbotUser.objects.get(id=creator_id)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid creator'}, status=status.HTTP_401_UNAUTHORIZED)

        # twillio response data api has specific fileds from serializers
        serializer = IncomingMessageSerializer(data=request.data)

        if serializer.is_valid():
            body = serializer.validated_data['Body']
            from_number = serializer.validated_data['From']
            print(request.data)
            if from_number.startswith('whatsapp:'):
                from_number = from_number[9:]
            # map customer to chatbot
            try:
                customer = Customer.objects.get(phone=from_number)
            except ObjectDoesNotExist:
                customer = Customer.objects.create(
                    phone=from_number, name=from_number, last_active=timezone.now())
                customer.users.add(creator)
                customer.save()

            try:
                # create message record in the database
                twilio_helper = TwilioHelper()

                is_first_and_message = twilio_helper.first_message_response(
                    body, chatbot, customer)

                if is_first_and_message:
                    response_message = is_first_and_message
                else:
                    faq = twilio_helper.fetch_matching_faq(
                        message=body, chatbot=chatbot)
                    response_message = faq
                    if not faq:
                        # send response from chatgpt
                        gpt_client = ChatGPTClient()
                        response_message = gpt_client.ask_question(body)

                user_message = Message.objects.create(
                    message=body, customer=customer, chatbot=chatbot)
                bot_message = Message.objects.create(
                    message=response_message, customer=customer, chatbot=chatbot, message_user=MessageUserTypeChoice.BOT)

                # Send a message to incoming number
                twilio_helper.send_whatsapp_message(
                    to_number=from_number, message_text=response_message)
                return Response(status=status.HTTP_200_OK, data={'message': 'Message object created', 'response_message': response_message, 'from_number': from_number, })

            except Exception as e:
                print(e)
                return Response({'error': f'Message object not created: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
