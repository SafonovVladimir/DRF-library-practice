import telegram

from typing import Type
from django.conf import settings
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from books.permissions import IsAdminOrReadOnly
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return BorrowingSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return self.serializer_class
     
    def get_queryset(self):
        user = self.request.user
        queryset = Borrowing.objects.all()

        if not user.is_staff:
            queryset = queryset.filter(user_id=user)

        is_active = self.request.query_params.get("is_active")
        if is_active:
            queryset = queryset.filter(actual_date=None)

        user_id = self.request.query_params.get("user_id")
        if user.is_staff and user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def perform_create(self, serializer):
        books = serializer.validated_data.get("book_id")
        for book in books:
            if book.inventory == 0:
                raise ValidationError("Book inventory is 0.")
            book.inventory -= 1
            book.save()

        serializer.save(user_id=self.request.user)


@api_view(['GET'])
def check_overdue_borrowings(request):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
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
