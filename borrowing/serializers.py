from rest_framework import serializers

from .models import Borrowing
from books.serializers import BookListSerializer



class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_date",
            "actual_date",
            "book_id",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book_id = BookListSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_date",
            "actual_date",
            "book_id",
        )
