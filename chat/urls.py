from django.urls import path

from . import views

urlpatterns = [
	path('', views.create_and_load_messages, name='create_and_load_messages'),
]