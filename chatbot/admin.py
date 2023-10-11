from django.contrib import admin

# Register your models here.
from .models import ChatbotUser, Chatbot


@admin.register(ChatbotUser)
class ChatbotUserAdmin(admin.ModelAdmin):
    # ordering = ['-modified']
    list_display = ('id', 'name', 'email')
    search_fields = ['name', 'email']


@admin.register(Chatbot)
class ChatbotAdmin(admin.ModelAdmin):
    ordering = ['-modified']
    list_display = ('id', 'user', )
