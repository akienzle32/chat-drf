from django.urls import path

from . import views

urlpatterns = [
	path('', views.load_messages, name='load_messages'),
	path('', views.create_message, name='create_message')
]