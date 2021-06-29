from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.request import Request
from django.views.decorators.http import last_modified
#from django.views.decorators.cache import cache_page

from rest_framework.parsers import JSONParser

from .models import Message
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .serializers import MessageSerializer
from datetime import datetime


#def login_view(request):
#	template = loader.get_template('login.html')
#	username = request.POST['username']
#	password = request.POST['password']
#	user = authenticate(request, username=username, password=password)
#	if user is not None:
#		login(request, User)
#	else:
#		return ("Invalid login.")	
		

def latest_message(request):
	return Message.objects.latest("timestamp").timestamp

#@login_required
@last_modified(latest_message)   
#@condition(last_modified_func=latest_message)	
def create_and_load_messages(request):
	if request.method == 'GET':
		messages = Message.objects.all()
		serializer = MessageSerializer(messages, many=True)
		response = JsonResponse(serializer.data, safe=False)
		response["Access-Control-Allow-Origin"] = "*"
		return response		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = MessageSerializer(data=data)
		if serializer.is_valid():
			serializer.save(author=request.user)
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)		
					