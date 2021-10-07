from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta

from .models import Chat, Participant, Message
from .serializers import ChatSerializer, ParticipantSerializer, MessageSerializer, UserSerializer


def login_user(request):
	if request.method != 'POST':
		return HttpResponse('Hello', status=200)
	else:
		username = request.POST.get('username')
		print(username)
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			serializer = UserSerializer(user);
			return JsonResponse(serializer.data, status=200)
		else:
			return HttpResponse(status=404)

def logout_user(request):
	logout(request)
	return HttpResponse(status=200)


def get_users(request):
	query = User.objects.all()
	serializer = UserSerializer(query, many=True)
	response = JsonResponse(serializer.data, safe=False)
	user = request.user
	if not user.is_superuser:
		return HttpResponse(status=401)
	else:
		return response

def get_current_user(request):
	user = request.user
	if user.is_anonymous:
		return HttpResponse(status=404)
	else:
		query = User.objects.get(username=user)
		serializer = UserSerializer(query)
		response = JsonResponse(serializer.data)
		#response["Access-Control-Allow-Origin"] = "*"
		return response

def get_all_chats(request):
	query = Chat.objects.all()
	serializer = ChatSerializer(query, many=True)
	response = JsonResponse(serializer.data, safe=False)
	user = request.user
	if not user.is_superuser:
		return HttpResponse(status=401)
	else:
		return response

def get_and_post_chats(request):
	if request.method == 'GET':
		user = request.user
		chatIds = Participant.objects.filter(name=user).values('chat_id')
		query = Chat.objects.filter(pk__in=chatIds)
		serializer = ChatSerializer(query, many=True)
		response = JsonResponse(serializer.data, safe=False)

		if user.is_authenticated:
			return response
		else:
			return HttpResponse(serializer.errors, status=401)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = ChatSerializer(data=data)
		if not serializer.is_valid():
			return HttpResponse(serializer.errors, status=400)
		else:
			user = request.user
			if not user.is_authenticated:
				return HttpResponse(status=401)
			else:
				serializer.save()
				return JsonResponse(serializer.data, status=201)
	else:
		return HttpResponse(status=400)

def get_patch_and_delete_chat(request, chat):
	user = request.user
	if request.method == 'GET':
		query = Chat.objects.get(pk=chat)
		serializer = ChatSerializer(query)
		response = JsonResponse(serializer.data)
		if user.is_authenticated:
			return response
	elif request.method == 'PUT':
		current_chat = Chat.objects.get(pk=chat)
		latest_message = Message.objects.filter(chat=current_chat).latest('timestamp')
		current_chat.last_modified = latest_message
		if not user.is_authenticated:
			return HttpResponse(status=401)
		else:
			current_chat.save()
			serializer = ChatSerializer(current_chat)
			return JsonResponse(serializer.data, status=201)
	elif request.method == 'DELETE':
		current_chat = Chat.objects.get(pk=chat)
		current_chat.delete()
		response_msg = 'Chat successfully deleted'
		return HttpResponse(response_msg, status=200)
	else:
		return HttpResponse(status=400)

def safe_get(username):
	try:
		return User.objects.get(username=username);
	except User.DoesNotExist:
		return None;

def get_and_post_participants(request):
	# Returns a list of the participants in all of a given user's chats.
	if request.method == 'GET':
		user = request.user
		chatIds = Participant.objects.filter(name=user).values('chat_id')
		query = Participant.objects.filter(chat__in=chatIds)
		serializer = ParticipantSerializer(query, many=True)
		response = JsonResponse(serializer.data, safe=False)

		if user.is_authenticated:
			return response
		else:
			return HttpResponse(status=401)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		chatId = data['chat']
		chat = Chat.objects.get(pk=chatId)
		username = data['name']
		new_participant = safe_get(username)

		if new_participant is None:
			return HttpResponse('Username does not exist', status=404)
		else:
			participant_query = Participant.objects.filter(chat=chat)
			participant_list = []
			for participant in participant_query:
				participant_list.append(participant.name)

			if new_participant in participant_list:
				return HttpResponse('Participant already in chat', status=400)
			else:
				serializer = ParticipantSerializer(data=data)
				if not serializer.is_valid():
					return HttpResponse(serializer.errors, status=400)	
				else:
					user = request.user
					if not user.is_authenticated:
						return HttpResponse(status=401)	
					else:
						serializer.save(chat=chat)
						return JsonResponse(serializer.data, status=201)
	else:
		return HttpResponse(status=400)
		
# Function to get the timestamp of the latest fulfilled POST request. This will be called by create_and_load_messages
# in order to determine if the full resource needs to be sent. 
def latest_message(request):
	return Message.objects.latest("timestamp").timestamp

  
def create_and_load_messages(request, chat):
	path = request.get_full_path()
	pathList = path.split('/')
	chatId = pathList[3]
	if request.method == 'GET':
		messages = Message.objects.filter(chat=chatId)
		recent_messages = messages.order_by('-id')[:20]
		recent_messages_sorted = reversed(recent_messages)
		serializer = MessageSerializer(recent_messages_sorted, many=True)
		response = JsonResponse(serializer.data, safe=False)
		#response["Access-Control-Allow-Origin"] = "*"
		user = request.user
		participant_list = []

		for participant in Participant.objects.filter(chat=chatId):
			participant_list.append(participant.name)

		if not user.is_authenticated or user not in participant_list:
			return HttpResponse(status=401)	
		else:
			if_modified_since = request.META.get('HTTP_IF_MODIFIED_SINCE')

			# This conditional accounts for the fact that the first GET request from the client will not include
			# an If-Modified-Since header, so that they can see the full resource on initial page load.
			if if_modified_since is None:
				return response
			else:
				parsed_date = parsedate_to_datetime(if_modified_since)

				# Only return the full resource if the database has received a message within the time indicated by the
				# 'If-Modified-Since' header.
				if latest_message(request) > parsed_date:
					return response
				# Otherwise, return Not Modified response. 	
				else:
					return HttpResponse(status=304)	
	elif request.method == 'POST':
		chat = Chat.objects.get(pk=chatId)
		data = JSONParser().parse(request)
		serializer = MessageSerializer(data=data)
		if not serializer.is_valid():
			return JsonResponse(serializer.errors, status=400)
		else:
			user = request.user
			# Only fulfill POST request if the user has logged in. If they have not, redirect them to the login page. 
			if not user.is_authenticated:
				return redirect('http://127.0.0.1:8000/accounts/login/')	
			else:
				serializer.save(author=user, chat=chat)
				return JsonResponse(serializer.data, status=201)
	else:
		return HttpResponse(status=400)


		