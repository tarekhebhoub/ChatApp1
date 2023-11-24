from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=('id','first_name','username','password','pic')
        extra_kwargs={'password':{'write_only':True}}

class SearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields=('id','first_name','username','pic')


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=('id','username','password','first_name','pic')
        extra_kwargs={'password':{'write_only':True}}

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Room
        fields='__all__'


class MessageSerializer(serializers.ModelSerializer):
       class Meta:
           model = models.Message
           fields = ('room', 'sender', 'content', 'timestamp')
           read_only_fields = ('timestamp',)