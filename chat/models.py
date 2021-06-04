from django.db import models

from django.contrib.auth import get_user_model

class Message(models.Model):
	author = models.CharField(max_length=200)
	timestamp = models.DateTimeField(auto_now_add=True)
	content = models.TextField()

	def __str__(self):
		return self.author.username

	def __str__(self):
		return self.timestamp

	def __str__(self):
		return self.content			

# Create your models here.
