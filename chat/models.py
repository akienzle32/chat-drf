from django.db import models

from django.contrib.auth.models import User

class Message(models.Model):
	author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add=True)
	content = models.TextField()

	#def __str__(self):
	#	return self.author.user.username

	#def __str__(self):
	#	return self.timestamp

	#def __str__(self):
	#	return self.content			

# Create your models here. 
