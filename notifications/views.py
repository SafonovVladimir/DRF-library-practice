import uuid

import telegram
import asyncio

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from library_config import settings
from notifications.models import TelegramUser

BOT_LINK = "https://t.me/CentralCityLibraryBot"


async def get_id_user_telegram(
        api_token: str,
        unique_identifier: str
) -> object:
    bot = telegram.Bot(token=api_token)
    updates = await bot.get_updates()
    for update in updates:
        if update.message.text.split()[-1] == unique_identifier:
            telegram_id = update.message.chat["id"]
            return telegram_id


class TelegramBotView(APIView):

    def get(self, request: Request) -> Response:
        unique_identifier = f"{uuid.uuid4()}"
        request.session["unique_identifier"] = unique_identifier
        bot_link = f"{BOT_LINK}?start={unique_identifier}"
        return Response({"bot_link": bot_link}, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        api_token = settings.TELEGRAM_BOT_TOKEN
        unique_identifier = request.session.get("unique_identifier")
        user_id = asyncio.run(get_id_user_telegram(
            api_token=api_token,
            unique_identifier=unique_identifier)
        )
        if user_id:
            if not TelegramUser.objects.filter(telegram_id=user_id).exists():
                TelegramUser.objects.create(telegram_id=user_id, user=request.user)
                return Response(
                    "You have successfully subscribed to notifications",
                    status=status.HTTP_200_OK
                )
            return Response(
                "You have already subscribed to notifications",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            "You have not provided a user ID to subscribe to notifications",
            status=status.HTTP_400_BAD_REQUEST
        )
