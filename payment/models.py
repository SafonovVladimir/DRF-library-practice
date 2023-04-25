from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        HARD = "PENDING"
        SOFT = "PAID"

    class TypeChoices(models.TextChoices):
        HARD = "PAYMENT"
        SOFT = "FINE"

    status = models.CharField(max_length=8, choices=StatusChoices.choices)
    type = models.CharField(max_length=8, choices=TypeChoices.choices)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)

    @property
    def amount(self):
        return (self.borrowing.book_id.daily_fee
                * (self.borrowing.actual_date
                   - self.borrowing.borrow_date).days)

    def __str__(self):
        return (f"For borrowing #{self.borrowing.id}\nStatus - {self.status} "
                f"({self.type}\nAmount of payment - ${self.amount}")
