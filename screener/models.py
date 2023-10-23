from django.db import models
from django.contrib.auth.models import AbstractUser


class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    security_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.symbol} | {self.security_name}"


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.username}"


class UserStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user} - {self.stock}"
