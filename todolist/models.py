from django.db import models
from django.contrib.auth.models import User


class ListNew(models.Model):
    item = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.item + '|' + str(self.completed)
