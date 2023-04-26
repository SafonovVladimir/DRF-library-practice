from datetime import date
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from books.serializers import BookBorrowingSerializer
from .models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="user_id.email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user_id",
            "borrow_date",
            "expected_date",
            "actual_date",
            "book_id",
        )
        read_only_fields = ("actual_date",)

    def validate(self, data):
        borrow_date = date.today()
        expected_date = data.get("expected_date")

        if expected_date and borrow_date and expected_date < borrow_date:
            raise serializers.ValidationError(_(
                "Expected date should be greater than borrow date."
            ))

        return data


class BorrowingDetailSerializer(BorrowingSerializer):
    book_id = BookBorrowingSerializer(many=True, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "user_id",
            "borrow_date",
            "expected_date",
            "actual_date",
            "book_id",
        )
