from django.db import models

from library_config.settings import AUTH_USER_MODEL


class TelegramUser(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    telegram_id = models.IntegerField()
