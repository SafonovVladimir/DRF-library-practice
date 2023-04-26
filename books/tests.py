from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from books.models import Book, Author
from books.serializers import BookListSerializer

BOOK_URL = reverse("book:book-list")


class AuthorModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="Test",
            last_name="Author",
            pseudonym="Test Pseudonym"
        )

    def test_author_str(self):
        self.assertEqual(
            str(self.author),
            "Test Author (Test Pseudonym)"
        )


class BookModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="Test",
            last_name="Author"
        )
        self.book = Book.objects.create(
            title="Test Book",
            cover=Book.CoverChoices.HARD,
            inventory=10,
            daily_fee=5
        )
        self.book.author.add(self.author)

    def test_book_str(self):
        self.assertEqual(
            str(self.book),
            "Test Book"
        )


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


class UnauthenticatedBooksApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AuthenticatedBooksApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "t1e2s3t4",
        )
        self.client.force_authenticate(self.user)
        self.author = Author.objects.create(
            first_name="Test",
            last_name="Author"
        )
        self.book = Book.objects.create(
            title="Test Book",
            cover=Book.CoverChoices.HARD,
            inventory=10,
            daily_fee=5
        )
        self.book.author.add(self.author)

    def test_list_books(self):
        sample_book()
        sample_book()

        res = self.client.get(BOOK_URL)

        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book(self):
        author = Author.objects.create(
            first_name="Sample",
            last_name="Author",
            pseudonym="Sample pseudonym"
        )

        payload = {
            "title": "Sample book",
            "author": author,
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 10,
        }

        res = self.client.post(BOOK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_book_filter_by_title(self):
        book_title_1 = sample_book(title="Test")
        book_title_2 = sample_book(title="132")
        book_title_3 = sample_book(title="")

        res = self.client.get(BOOK_URL, {"title": "Test"})

        serializer_1 = BookListSerializer(book_title_1)
        serializer_2 = BookListSerializer(book_title_2)
        serializer_3 = BookListSerializer(book_title_3)

        self.assertIn(serializer_1.data, res.data)
        self.assertNotIn(serializer_2.data, res.data)
        self.assertNotIn(serializer_3.data, res.data)

        res = self.client.get(BOOK_URL, {"title": ""})

        self.assertIn(serializer_1.data, res.data)
        self.assertIn(serializer_2.data, res.data)
        self.assertIn(serializer_3.data, res.data)

    def test_list_book_filter_by_author(self):
        book_author_1 = sample_book()
        book_author_2 = sample_book()
        book_author_3 = sample_book()

        author_1 = sample_author(
            first_name="John", last_name="Rowling", pseudonym="J. Rowling"
        )
        author_2 = sample_author()

        book_author_1.author.add(author_1)
        book_author_2.author.add(author_2)

        res = self.client.get(
            BOOK_URL, {"author": author_1.id}
        )

        serializer_1 = BookListSerializer(book_author_1)
        serializer_2 = BookListSerializer(book_author_2)
        serializer_3 = BookListSerializer(book_author_3)

        self.assertIn(serializer_1.data, res.data)
        self.assertNotIn(serializer_2.data, res.data)
        self.assertNotIn(serializer_3.data, res.data)

        res = self.client.get(BOOK_URL, {"author": ""})

        self.assertIn(serializer_1.data, res.data)
        self.assertIn(serializer_2.data, res.data)
        self.assertIn(serializer_3.data, res.data)

    def test_list_book_filter_by_cover(self):
        book_cover_1 = sample_book(cover="HARD")
        book_cover_2 = sample_book(cover="SOFT")
        book_cover_3 = sample_book(cover="")

        res = self.client.get(
            BOOK_URL, {"cover": "HARD"}
        )

        serializer_1 = BookListSerializer(book_cover_1)
        serializer_2 = BookListSerializer(book_cover_2)
        serializer_3 = BookListSerializer(book_cover_3)

        self.assertIn(serializer_1.data, res.data)
        self.assertNotIn(serializer_2.data, res.data)
        self.assertNotIn(serializer_3.data, res.data)

        res = self.client.get(BOOK_URL, {"cover": "SOFT"})

        self.assertNotIn(serializer_1.data, res.data)
        self.assertIn(serializer_2.data, res.data)
        self.assertNotIn(serializer_3.data, res.data)

        res = self.client.get(BOOK_URL, {"cover": ""})

        self.assertIn(serializer_1.data, res.data)
        self.assertIn(serializer_2.data, res.data)
        self.assertIn(serializer_3.data, res.data)


class AdminBookTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "t1e2s3t4",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        author = sample_author()

        payload = {
            "title": "Sample book",
            "author": author.id,
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 10,
        }

        res = self.client.post(BOOK_URL, payload)
        book = Book.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            if key == "author":
                self.assertEqual(author, book.author.first())
            else:
                self.assertEqual(payload[key], getattr(book, key))
