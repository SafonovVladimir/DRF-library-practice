from typing import Type

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.serializers import Serializer

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return BorrowingSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return self.serializer_class
