import telebot

from django.conf import settings
from django.utils import timezone
from rest_framework.response import Response

from borrowing.models import Borrowing


def check_overdue_borrowings():
    bot = telebot.TeleBot(token=settings.TELEGRAM_BOT_TOKEN)
    borrowings = Borrowing.objects.filter(
        expected_date__lte=timezone.now(),
        actual_date__isnull=False
    )
    for borrowing in borrowings:
        message = (f"Book '{list(borrowing.book_id.all())}' is overdue for "
                   f"{borrowing.user_id.first_name} "
                   f"{borrowing.user_id.last_name}. Borrowed on "
                   f"{borrowing.borrow_date.strftime('%Y-%m-%d')}, "
                   f"expected to return on "
                   f"{borrowing.expected_date.strftime('%Y-%m-%d')}.")
        bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=message)

    return Response({"message": f"Overdue borrowings checked."})
