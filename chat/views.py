#from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

#from rest_framework import generics
from rest_framework.parsers import JSONParser

from .models import Message
from .serializers import MessageSerializer

#class ChatView(generics.CreateAPIView):
#	queryset = Message.objects.all()
#	serializer_class = MessageSerializer


#list all messages, or create a new message

def message_log(request):
	if request.method == 'GET':
		messages = Message.objects.all()
		serializer = MessageSerializer(messages)
		return JsonResponse(serializer.data)

	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = MessageSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=201)
		return JsonResponse(serializer.errors, status=400)				
