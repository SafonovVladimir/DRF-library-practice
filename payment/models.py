from django.db import models

from borrowing.models import Borrowing

FINE_MULTIPLIER = 2


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        HARD = "PENDING"
        SOFT = "PAID"

    class TypeChoices(models.TextChoices):
        HARD = "PAYMENT"
        SOFT = "FINE"

    status = models.CharField(max_length=8, choices=StatusChoices.choices)
    type = models.CharField(max_length=8, choices=TypeChoices.choices)
    borrowing = models.OneToOneField(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField(default="www.kostyl.com")
    session_id = models.CharField(max_length=255, default="www.kostyl.com")

    @property
    def amount(self):
        extra_days = 0
        total_fee = 0

        # After merge change to daily_fee
        for book in self.borrowing.book_id.all():
            total_fee = book.daylee_fee

        if not self.borrowing.actual_date:
            days = (self.borrowing.expected_date
                    - self.borrowing.borrow_date).days
        else:
            if self.borrowing.actual_date > self.borrowing.expected_date:
                extra_days = (self.borrowing.actual_date
                              - self.borrowing.expected_date).days
                days = (self.borrowing.expected_date
                        - self.borrowing.borrow_date).days
            else:
                days = (self.borrowing.actual_date
                        - self.borrowing.borrow_date).days

        amount = days * total_fee + extra_days * total_fee * FINE_MULTIPLIER

        return amount

    def __str__(self):
        return (f"Payment #{self.id} for borrowing #{self.borrowing.id}\n"
                f"Status - {self.status} "
                f"({self.type}\nAmount of payment - ${self.amount})")

    class Meta:
        ordering = ("id", )
