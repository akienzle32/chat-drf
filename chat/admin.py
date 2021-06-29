from django.contrib import admin

from .models import Message

admin.site.register(Message)

admin.site.site_url = 'http://127.0.0.1:3000/'

# Register your models here.
