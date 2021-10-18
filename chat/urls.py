from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
	path('messages/<int:chat>', views.create_and_load_messages, name='create_and_load_messages'),
	path('users', views.get_users, name='get_users'),
	path('participants', views.get_and_post_participants, name='get_and_post_participants'),
	path('participants/<int:chat>', views.delete_participant, name='delete_participant'),
	path('chats', views.get_and_post_chats, name='get_and_post_chats'),
	path('chats/<int:chat>', views.get_patch_and_delete_chat, name='get_patch_and_delete_chat'),
	path('register', views.simple_register_new_user, name='simple_register_new_user'),
	path('api-token-auth/', obtain_auth_token, name='api_token_auth'), 
	path('', views.get_all_chats, name='get_all_chats')
]