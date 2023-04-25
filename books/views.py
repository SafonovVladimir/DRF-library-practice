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

    @staticmethod
    def _params_to_ints(qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the books with filters"""
        title = self.request.query_params.get("title")
        authors = self.request.query_params.get("authors")
        cover = self.request.query_params.get("cover")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if authors:
            authors_ids = self._params_to_ints(authors)
            queryset = queryset.filter(authors__id__in=authors_ids)

        if cover:
            cover_ids = self._params_to_ints(cover)
            queryset = queryset.filter(cover__id__in=cover_ids)

        return queryset.distinct()
