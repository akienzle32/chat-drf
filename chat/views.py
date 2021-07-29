from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.request import Request
#from django.views.decorators.http import last_modified
#from django.views.decorators.cache import cache_page

from rest_framework.parsers import JSONParser

from .models import Message
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
#from django.views.decorators.cache import cache_control 
from .serializers import MessageSerializer
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta
		

def latest_message(request):
	return Message.objects.latest("timestamp").timestamp
  
#@cache_control(max_age=300)
def create_and_load_messages(request):
	if request.method == 'GET':
		messages = Message.objects.all()
		serializer = MessageSerializer(messages, many=True)
		response = JsonResponse(serializer.data, safe=False)
		response["Access-Control-Allow-Origin"] = "*"
		user = request.user
		if user.is_authenticated:
			if_modified_since = request.META.get('HTTP_IF_MODIFIED_SINCE')
			parsed_date = parsedate_to_datetime(if_modified_since)
			if latest_message(request) > parsed_date or (datetime.now() - timedelta(seconds=2)) > user.last_login:
				return response
			else:
				return HttpResponse(status=304)		
		else:
			return HttpResponse(status=401)		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = MessageSerializer(data=data)
		if serializer.is_valid():
			user = request.user
			if user.is_authenticated:
				serializer.save(author=user)
				return JsonResponse(serializer.data, status=201)
			else:
				return redirect('http://127.0.0.1:8000/accounts/login/')	
		return JsonResponse(serializer.errors, status=400)		
					