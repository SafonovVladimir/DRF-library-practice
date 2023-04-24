from django.db import models


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD"
        SOFT = "SOFT"

    title = models.CharField(max_length=63)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=63, choices=CoverChoices.choices)
    image = models.ImageField(upload_to="book_cover", blank=True, null=True)
    inventory = models.IntegerField()
    daylee_fee = models.IntegerField()
