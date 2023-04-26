from rest_framework import serializers

from books.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = (
            "first_name",
            "last_name",
            "pseudonym",
        )


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "image",
            "inventory",
            "daily_fee"
        )


class BookListSerializer(BookSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "inventory", "daily_fee")


class BookBorrowingSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ("title", "author",)
