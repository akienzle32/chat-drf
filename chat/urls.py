from django.urls import path

from . import views

urlpatterns = [
	path('messages/<int:chat>', views.create_and_load_messages, name='create_and_load_messages'),
	path('current-user', views.get_current_user, name='get_current_user'),
	path('users', views.get_users, name='get_users'),
	path('participants', views.get_and_post_participants, name='get_and_post_participants'),
	path('', views.get_and_post_chats, name='get_and_post_chats'),
]