#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.request import Request
from django.views.decorators.http import last_modified

#from rest_framework import generics
from rest_framework.parsers import JSONParser

from .models import Message
from django.contrib.auth.models import User
from .serializers import MessageSerializer

#class ChatView(generics.CreateAPIView):
#	queryset = Message.objects.all()
#	serializer_class = MessageSerializer


#list all messages, or create a new message	

def latest_message(request):
    return Message.objects.latest("timestamp").timestamp

@last_modified(latest_message)
def load_messages(request):
	if request.method == 'GET':
		messages = Message.objects.all()
		serializer = MessageSerializer(messages, many=True)
		response = JsonResponse(serializer.data, safe=False)
		response["Access-Control-Allow-Origin"] = "*"
		return response	

def create_message(request):
	if request.method == 'POST':
		serializer = MessageSerializer(data=request.POST)
		if serializer.is_valid():
			#Message.objects.create()
			serializer.save()
			return HttpResponse(serializer.data, status=201)
		return HttpResponse(serializer.errors, status=400)						

#request.GET.get('param1', None)