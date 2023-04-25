from django.db import models

from books.models import Book
from user.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_date = models.DateField()
    actual_date = models.DateField(blank=True, null=True)
    book_id = models.ManyToManyField(Book, related_name="borrowings")
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID-{self.id} ({self.borrow_date}-{self.expected_date})"
