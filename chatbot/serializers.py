from rest_framework import serializers
from .models import ChatbotUser, Chatbot, Questions, Message
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotUser
        fields = ['id', 'name', 'email', ]

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            # extra_kwargs = {'password': {'write_only': True}}
            raise serializers.ValidationError("Invalid email address.")
        return value

    def create(self, validated_data):
        baseuser = User.objects.create(
            username=validated_data['email'],
            password=self.context['request'].data['password']
        )
        user = ChatbotUser.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            user=baseuser
        )
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['id', 'question', 'answer', 'chatbot_id']

    def create(self, validated_data):
        # Get chatbot_id from validated data
        chatbot_id = self.context['request'].data.get('chatbot_id')

        if chatbot_id is None:
            raise serializers.ValidationError("chatbot_id is required")

        try:
            chatbot = Chatbot.objects.get(id=chatbot_id)
        except Chatbot.DoesNotExist:
            raise serializers.ValidationError("Invalid chatbot_id")

        question = Questions.objects.create(chatbot=chatbot, question = validated_data["question"], answer= validated_data["answer"])
        return question


class ChatbotSerializer(serializers.ModelSerializer):
    questions = QuestionsSerializer(many=True, read_only=True)

    class Meta:
        model = Chatbot
        fields = ['id', 'name', 'type', 'greet_template', 'questions']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'message', 'customer', 'chatbot', 'created']
        ordering = ['-created']

class IncomingMessageSerializer(serializers.Serializer):
    Body = serializers.CharField()
    From = serializers.CharField()
    