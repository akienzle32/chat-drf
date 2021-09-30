from django.urls import path

from . import views

urlpatterns = [
	path('messages/<int:chat>', views.create_and_load_messages, name='create_and_load_messages'),
	path('user', views.get_user, name='get_user'),
	path('participants', views.get_and_post_participants, name='get_and_post_participants'),
	path('', views.get_and_post_chats, name='get_and_post_chats'),
]