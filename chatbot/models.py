from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    condition = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    statement = models.CharField(max_length=255, default = '1')

    def __str__(self):
        return f'{self.user}: {self.message}'