from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password1 = models.CharField(max_length=128)
    password2 = models.CharField(max_length=128)


    def __str__(self) -> str:
        return self.username