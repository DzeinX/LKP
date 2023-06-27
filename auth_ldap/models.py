from django.contrib.auth.models import AbstractUser
from django.db import models

from Config import ModelLists

positions_at_work = ModelLists.positions


class Positions(models.Model):
    position = models.CharField(max_length=40, choices=positions_at_work, default=ModelLists.positions[0][0])


class User(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    full_name = models.CharField(max_length=60)
    is_active = models.BooleanField()

    position_at_work = models.ForeignKey(Positions, on_delete=models.SET_NULL, null=True)

    def __repr__(self):
        return f'<User {self.username}>'
