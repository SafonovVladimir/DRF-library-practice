from typing import Type

from rest_framework import viewsets
from rest_framework.serializers import Serializer

from books.models import Book
from books.permissions import IsAdminOrReadOnly
from books.serializers import (
    BookSerializer,
    BookListSerializer
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return BookListSerializer
        return self.serializer_class
