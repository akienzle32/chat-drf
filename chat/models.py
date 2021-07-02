from django.db import models

from django.contrib.auth.models import User

class Message(models.Model):
	author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	content = models.TextField()		

# Create your models here. 
