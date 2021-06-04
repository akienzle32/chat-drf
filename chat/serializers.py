from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'author', 'timestamp', 'content')

        def create(self, validated_data):
        	return Message.objects.create(**validated_data)

        def update(self, instance, validated_data):
        	instance.author = validated_data.get('author', instance.username)
        	instance.author = validated_data.get('timestamp', instance.timestamp)
        	instance.content = validated_data.get('content', instance.content)
        	instance.save()
        	return instance	    