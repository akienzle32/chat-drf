from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta

from .models import Message
from .serializers import MessageSerializer
		
# Function to get the timestamp of the latest fulfilled POST request. This will be called by create_and_load_messages
# in order to determine if the full resource needs to be sent. 
def latest_message(request):
	return Message.objects.latest("timestamp").timestamp
  
def create_and_load_messages(request):
	if request.method == 'GET':
		messages = Message.objects.all()
		serializer = MessageSerializer(messages, many=True)
		response = JsonResponse(serializer.data, safe=False)
		response["Access-Control-Allow-Origin"] = "*"
		user = request.user

		# Only fulfill GET request if the user has logged in.
		if user.is_authenticated:
			if_modified_since = request.META.get('HTTP_IF_MODIFIED_SINCE')
			parsed_date = parsedate_to_datetime(if_modified_since)

			# Only return the full resource if the database has received a message within the time indicated by the
			# 'If-Modified-Since' header OR if the user has recently logged in. 
			if latest_message(request) > parsed_date or user.last_login > (datetime.now() - timedelta(seconds=2)):
				return response
			#Otherwise, return Not Modified response. 	
			else:
				return HttpResponse(status=304)		
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


		