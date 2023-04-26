from django.urls import path

from notifications.views import TelegramBotView

urlpatterns = [
    path("telegram-bot/", TelegramBotView.as_view(), name="telegram-bot"),
]

app_name = "notification"
