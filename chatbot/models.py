from django.db import models
from uuid import uuid4
from django_extensions.db.models import TimeStampedModel
from .model_helpers import CountryChoice, ChatBotTypesChoice, MessageUserTypeChoice
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

class ChatbotUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chatbot_user')


    def __str__(self):
        if not self.name:
            return self.id
        return self.name

class Customer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    users = models.ManyToManyField(ChatbotUser,related_name='customer_details') 
    last_active = models.DateTimeField()
    country = models.CharField(
        max_length=30, choices=CountryChoice.choices, default=CountryChoice.INDIA)

    def __str__(self):
        if not self.name:
            return self.id
        return self.name


class Chatbot(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=ChatBotTypesChoice.choices, default=ChatBotTypesChoice.CUSTOMER_SUPPORT)
    greet_template = models.TextField()
    user = models.ForeignKey(ChatbotUser, on_delete=models.CASCADE, related_name='chatbots')

    def __str__(self):
        return f'Chatbot {self.id}'
    
    
class Questions(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    question = models.TextField()
    answer = models.TextField()
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE, related_name='questions')
    
    def __str__(self):
        return f'Question {self.id}'

class Message(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    message = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='all_messages')
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE, related_name='all_messages')
    message_user = models.CharField(max_length=100, choices=MessageUserTypeChoice.choices, default=MessageUserTypeChoice.CUSTOMER)
    
    def __str__(self):
        return f'Message {self.id}'

    