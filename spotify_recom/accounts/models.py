from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)


    def __str__(self) -> str:
        return self.username