from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.conf import settings

class Acc(AbstractUser):
    phone = models.CharField(max_length=20)
    username = models.CharField(max_length=20,unique=True)
    invite_code = models.CharField(max_length=6, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    recommended_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE, blank=True,
                                       null=True, related_name='rec_by')
    def __str__(self):
        return f'Пользователь: {self.username} - Инвайт от {self.invite_code}'



class Passcode(models.Model):
    passcode = models.TextField(max_length=6)


