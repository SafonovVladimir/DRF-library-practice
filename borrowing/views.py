from typing import Type

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.serializers import Serializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from books.permissions import IsAdminOrReadOnly
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingDetailSerializer


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

    def perform_create(self, serializer):
        book = serializer.validated_data.get("book_id")
        if book.inventory == 0:
            raise ValidationError("Book inventory is 0.")

        book.inventory -= 1
        book.save()

        serializer.save(user_id=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = Borrowing.objects.all()

        if not user.is_staff:
            queryset = queryset.filter(user_id=user)

        is_active = self.request.query_params.get("is_active")
        if is_active:
            queryset = queryset.filter(actual_date=None)


