from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'user_name', 'pub_date', 'content')

        def create(self, validated_data):
        	return Message.objects.create(**validated_data)

        def update(self, instance, validated_data):
        	instance.user_name = validated_data.get('user_name', instance.user_name)
        	instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        	instance.content = validated_data.get('content', instance.content)
        	instance.save()
        	return instance	    