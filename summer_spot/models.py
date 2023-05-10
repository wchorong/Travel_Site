from django.db import models
from user_set.models import User

# Create your models here.
class Post(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    region = models.CharField(max_length=50, blank=True) # 지역
    user = models.ForeignKey(User, on_delete=models.CASCADE)