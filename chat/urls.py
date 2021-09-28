from django.urls import path

from . import views

urlpatterns = [
	path('messages', views.create_and_load_messages, name='create_and_load_messages'),
	path('user', views.get_user, name='get_user'),
	path('', views.get_chats, name='get_chats'),
]