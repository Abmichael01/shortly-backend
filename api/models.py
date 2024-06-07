from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Url(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,  editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=300)
    keyword = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)
    
    def __str__(self):
        return self.url

class Click(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=20)
    location = models.CharField(max_length=50)

    def __str__(self):
        return str(self.ip_address) + ': ' + str(self.location)