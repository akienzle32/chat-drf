from rest_framework import serializers
from .models import Message, Participant, Chat
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ChatSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    class Meta:
        model = Chat
        fields = ['id', 'name']

        def create(self, validated_data):
            return ChatSerializer.create(**validated_data)


class ParticipantSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    chat = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Participant
        fields = ['id', 'name', 'chat']

        def create(self, validated_data):
            return ParticipantSerializer.create(**validated_data)


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), required=False, allow_null=True, slug_field='username')

    class Meta:
        model = Message
        fields = ('id', 'author', 'timestamp', 'content')
        #exclude = ['author']

        def create(self, validated_data):
        	return Message.objects.create(**validated_data)