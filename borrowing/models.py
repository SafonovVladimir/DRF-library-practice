from django.db import models

from books.models import Book
from user.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_date = models.DateField()
    actual_date = models.DateField()
    book_id = models.ManyToManyField(Book, related_name="borrowings")
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.book_id.title}"
                f"({self.borrow_date}-{self.expected_date})")
