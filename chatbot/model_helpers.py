from django.db import models


class CountryChoice(models.TextChoices):
    INDIA = 'INDIA', 'INDIA'
    USA = 'USA', 'USA'
    UK = 'UK', 'UK'
    OTHERS = 'OTHERS', 'OTHERS'


class ChatBotTypesChoice(models.TextChoices):
    CUSTOMER_SUPPORT = 'CUSTOMER_SUPPORT', 'CUSTOMER_SUPPORT'
    SALES = 'SALES', 'SALES'
    PRODUCT_RECOMENDATION = 'PRODUCT_RECOMENDATION', 'PRODUCT_RECOMENDATION'
    WELCOME = 'WELCOME', 'WELCOME'


class MessageUserTypeChoice(models.TextChoices):
    BOT = 'BOT', 'BOT'
    AGENT = 'AGENT', 'AGENT'
    CUSTOMER = 'CUSTOMER', 'CUSTOMER'
