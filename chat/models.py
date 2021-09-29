from django.db import models

from django.contrib.auth.models import User

DEFAULT_CHAT_PK = 1;

class Chat(models.Model):
	name = models.CharField(max_length=50)


class Participant(models.Model):
	name = models.ForeignKey(User, on_delete=models.CASCADE)
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

class Message(models.Model):
	author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE, default=DEFAULT_CHAT_PK)

# Create your models here. 
