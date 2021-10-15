from django.urls import path

from . import views


urlpatterns = [
	path('messages/<int:chat>', views.create_and_load_messages, name='create_and_load_messages'),
	path('current-user', views.get_current_user, name='get_current_user'),
	path('users', views.get_users, name='get_users'),
	path('participants', views.get_and_post_participants, name='get_and_post_participants'),
	path('participants/<int:chat>', views.delete_participant, name='delete_participant'),
	path('chats', views.get_and_post_chats, name='get_and_post_chats'),
	path('chats/<int:chat>', views.get_patch_and_delete_chat, name='get_patch_and_delete_chat'),
	path('login', views.login_user, name='login_user'),
	path('logout', views.logout_user, name='logout_user'),
	path('register', views.simple_register_new_user, name='simple_register_new_user'),
	path('token', views.get_csrf_token, name='get_csrf_token'),
	path('', views.get_all_chats, name='get_all_chats')
]