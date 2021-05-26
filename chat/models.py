from django.db import models

class Message(models.Model):
	user_name = models.CharField(max_length=200)
	pub_date = models.DateTimeField()
	content = models.TextField()

	def __str__(self):
		return self.user_name

	def __str__(self):
		return self.pub_date

	def __str__(self):
		return self.content			

# Create your models here.
