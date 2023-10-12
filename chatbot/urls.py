from django.urls import path
from .views import UserSignupView, UserLoginView, MessageCreateView, MessageRetrieveView, ChatbotCreateView, ChatbotRetrieveView, QuestionsCreateView, QuestionsListView, TwilioWebhookView, ChatbotUpdateView, QuestionsUpdateView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('messages/', MessageCreateView.as_view(), name='message-create'),
    path('messages/list/', MessageRetrieveView.as_view(), name='message-detail'),
    path('chatbots/', ChatbotCreateView.as_view(), name='chatbot-create'),
    path('chatbots/<uuid:pk>/', ChatbotRetrieveView.as_view(), name='chatbot-detail'),
    path('chatbots/<uuid:chatbot_id>/questions/',
         QuestionsCreateView.as_view(), name='questions-create'),
    path('chatbots/<uuid:pk>/update/',
         ChatbotUpdateView.as_view(), name='chatbot-update'),
    path('chatbots/<uuid:chatbot_id>/questions/list/',
         QuestionsListView.as_view(), name='questions-list'),
    path('chatbots/<uuid:pk>/questions/update/',
         QuestionsUpdateView.as_view(), name='questions-update'),
    path('twilio_webhook/', TwilioWebhookView.as_view(), name='twilio_webhook'),
]
