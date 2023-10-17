from twilio.rest import Client
from django.conf import settings
from .models import Chatbot, Message, Customer
from fuzzywuzzy import process


class TwilioHelper:
    """
        setup twillio webhook for message store, process and respond.
    """
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID,
                             settings.TWILIO_AUTH_TOKEN)

    def send_whatsapp_message(self, to_number, message_text):
        print(message_text)
        message = self.client.messages.create(
            from_='whatsapp:' + settings.TWILIO_PHONE_NUMBER,
            body=message_text,
            to='whatsapp:' + to_number
        )
        return message

    def find_most_matching_question(self, questions, provided_answer):
        best_match, score = process.extractOne(provided_answer, questions)
        return best_match, score

    def first_message_response(self, message: str, chatbot: Chatbot, customer: Customer):
        response_message = chatbot.greet_template
        # greet template should be like:
        # Hello{name}, my name is  {chatbot_name}! I am a {{chatbot_type}}. How can I help you?

        # check if its first message
        
        if message.startswith("Hi") or message.startswith("Hello") or message.startswith("Hey"):
            return chatbot.greet_template
                    
        try:
            messages = Message.objects.filter(customer__phone=customer.phone, chatbot=chatbot)
            if messages.count() == 0:
                return chatbot.greet_template
        except:
            return 
        if chatbot.all_messages.count() == 0:
            return chatbot.greet_template
        else:
            return
        
    # best match from the list of available questions
    def fetch_matching_faq(self, message, chatbot):
        questions_ans = chatbot.questions.all().values_list('question', 'answer',)
        quest = [q[0] for q in questions_ans]
        best_match, score = self.find_most_matching_question(
            quest, message)

        # print(best_match, questions_ans)
        if score > 80:
            ans = ''
            for q in questions_ans:
                if q[0] == best_match:
                    ans = q[1]
            return ans
        return None
