from datetime import date, timedelta

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse

from books.models import Author, Book
from borrowing.models import Borrowing
from user.models import User

BORROW_URL = reverse("borrowing:borrowing-list")


class UnauthenticatedBorrowingsApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


def sample_user(email="test@test.com", password="t1e2s3t4"):
    """Creating test user"""
    return User.objects.create_user(email, password)


def sample_author(**params):
    defaults = {
        "first_name": "Test",
        "last_name": "Author",
        "pseudonym": "TA"
    }
    defaults.update(params)
    return Author.objects.create(**defaults)


def sample_book(**params):
    defaults = {
        "title": "Sample Book",
        "cover": Book.CoverChoices.HARD,
        "inventory": 10,
        "daily_fee": 2
    }
    author = params.pop("author", None)
    if author is None:
        author = sample_author()
    defaults.update(params)
    book = Book.objects.create(**defaults)
    book.author.add(author)
    return book


class AuthenticatedBorrowingsApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "t1e2s3t4",
        )
        self.client.force_authenticate(self.user)

    def test_list_borrowings(self):
        res = self.client.get(BORROW_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_create_borrowing(self):
    #     book = sample_book()
    #     payload = {
    #         "borrow_date": "2020-01-01",
    #         "expected_date": "2021-01-04",
    #         "actual_date": "2021-01-01",
    #         "book": book.id,
    #         "user_id": self.user.id
    #     }
    #     res = self.client.post(BORROW_URL, payload)
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
