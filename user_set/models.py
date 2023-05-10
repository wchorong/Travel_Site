from django.db import models

class User(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(unique=True)

    def __str__(self):
        return self.nickname