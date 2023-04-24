# Generated by Django 4.1 on 2023-04-24 11:03

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=63)),
                ("author", models.CharField(max_length=255)),
                (
                    "cover",
                    models.CharField(
                        choices=[("HARD", "Hard"), ("SOFT", "Soft")], max_length=63
                    ),
                ),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="book_cover"),
                ),
                ("inventory", models.IntegerField()),
                ("daylee_fee", models.IntegerField()),
            ],
        ),
    ]