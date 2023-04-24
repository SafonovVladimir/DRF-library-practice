from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)
    pseudonim = models.CharField(max_length=63, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.pseudonim})"


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD"
        SOFT = "SOFT"

    title = models.CharField(max_length=63)
    author = models.ManyToManyField(Author, related_name="books")
    cover = models.CharField(max_length=63, choices=CoverChoices.choices)
    image = models.ImageField(upload_to="book_cover", blank=True, null=True)
    inventory = models.IntegerField()
    daily_fee = models.IntegerField()

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ("title",)
