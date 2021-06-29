from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'messages']

class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), required=False, allow_null=True, slug_field='username')

    class Meta:
        model = Message
        fields = ('id', 'author', 'timestamp', 'content')
        #exclude = ['author']

        def create(self, validated_data):
        	return Message.objects.create(**validated_data)

        #def update(self, instance, validated_data):
        #	instance.author = validated_data.get('author', instance.user.username)
        #	instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        #	#instance.content = validated_data.get('content', instance.content)
        #	#instance.save()
        #	return instance	    