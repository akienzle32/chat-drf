from django.urls import path

from . import views

urlpatterns = [
	path('', views.message_log, name='message_log')
]