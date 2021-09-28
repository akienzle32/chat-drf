from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta

from .models import Chat, Participant, Message
from .serializers import ChatSerializer, ParticipantSerializer, MessageSerializer, UserSerializer


def get_chats(request):
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
	else:
		return HttpResponse(status=400)


def get_user(request):
	if request.method == 'GET':
		user = request.user
		query = User.objects.get(username=user)
		serializer = UserSerializer(query)
		response = JsonResponse(serializer.data)
		#response["Access-Control-Allow-Origin"] = "*"

		if user.is_authenticated:
			return response
		else:
			return HttpResponse(status=401)
	else:
		return HttpResponse(status=400)


def get_participants(request):
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
	else:
		return HttpResponse(status=400)
		
# Function to get the timestamp of the latest fulfilled POST request. This will be called by create_and_load_messages
# in order to determine if the full resource needs to be sent. 
def latest_message(request):
	return Message.objects.latest("timestamp").timestamp
  
def create_and_load_messages(request):
	if request.method == 'GET':
		recent_messages = Message.objects.all().order_by('-id')[:20]
		recent_messages_sorted = reversed(recent_messages)
		serializer = MessageSerializer(recent_messages_sorted, many=True)
		response = JsonResponse(serializer.data, safe=False)
		response["Access-Control-Allow-Origin"] = "*"
		user = request.user

		# Only fulfill GET request if the user has logged in.
		if user.is_authenticated:
			return response
		else:
			return HttpResponse(status=401)		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = MessageSerializer(data=data)
		if serializer.is_valid():
			user = request.user
			#Only fulfill POST request if the user has logged in. If they have not, redirect them to the login page. 
			if user.is_authenticated:
				serializer.save(author=user)
				return JsonResponse(serializer.data, status=201)
			else:
				# Maybe just make this a standard 401 response(?)
				return redirect('http://127.0.0.1:8000/accounts/login/')	
		return JsonResponse(serializer.errors, status=400)	


		