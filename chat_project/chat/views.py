from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from . import serializers
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.db.models import Q
from django.contrib.auth import authenticate

from . import models
# Create your views here.

def hello(request):
	print("tarek")
	return Response({"tarek"})

class UserCreate(APIView):
	# self.userModel=get_user_model()
    permission_classes=()
    serializer_class=serializers.UserSerializer
    def post(self,request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.create_user(**serializer.validated_data)
            token=Token.objects.create(user=user)
            serializer = serializers.UserSerializer(user)
            data=serializer.data
            data["token"]=str(user.auth_token.key)
            print(data)
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes=()
    serializer_class=serializers.LoginSerializer
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")
        user=authenticate(username=username,password=password)
        if user:
            # refresh = RefreshToken.for_user(user)
            try:
                Token.objects.create(user=user)
            except:
                Token.objects.filter(user=user).delete()
                Token.objects.create(user=user)
            serializer = serializers.LoginSerializer(user)
            data=serializer.data
            data['token']=str(user.auth_token.key)
            print(data)

            return Response(data)
            return Response({
                "token":str(user.auth_token.key),
                "username":user.username,
                # "pic":user.pic,
                "first_name":user.first_name
                },status=status.HTTP_200_OK)
        else:
            return Response({"error":"Wrong Credentials"},status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({"Logout successfully"},status=status.HTTP_200_OK)


class RoomView(APIView):
    # self.userModel=get_user_model()
    # permission_classes=()
    serializer_class=serializers.UserSerializer
    def post(self,request):
        user=request.user
        user2=request.data['userId']
        
        room=models.Room.objects.filter(users=user.id).filter(users=user2).first()
        print(room)
        if room:
            serializer=serializers.RoomSerializer(room)
            full_users_list = list(get_user_model().objects.filter(id__in=room.users.all()))
            print(full_users_list)
            data=serializer.data
            userSerializer=serializers.UserSerializer(full_users_list,many=True)
            data["users"]=userSerializer.data
            return Response(data)

        roomData={
            'name_room':'sender',
        }
        room=models.Room.objects.create(**roomData)
        room.users.set([user.id,user2])
        serializer=serializers.RoomSerializer(room)
        return Response(serializer.data)

        # request.data['owner']=user.id
        # request.data['users']=[user.id]
        # serializer = serializers.RoomSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data,status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=400)
    def get(self,request):
        user=request.user
        print(user)
        rooms=models.Room.objects.filter(users=user.id)
        serializer=serializers.RoomSerializer(rooms,many=True)
        data=serializer.data
        i=0
        for room in rooms:
            full_users_list = list(get_user_model().objects.filter(id__in=room.users.all()))
            userSerializer=serializers.UserSerializer(full_users_list,many=True)
            data[i]['users']=userSerializer.data
            i+=1
        return Response(data)

class MessageView(APIView):
    def post(self,request,id_room):
        data=request.data
        data['sender']=request.user.id
        data['room']=id_room
        serializer=serializers.MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def get(self,request,id_room):
        # room=models.objects.get(id=id_room)
        messages=models.Message.objects.filter(room=id_room)
        serializer=serializers.MessageSerializer(messages,many=True)
        return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tryToken(request):
    return Response({'tarek'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchUsers(request):
    search_param = request.GET.get('search', '')

    users=models.User.objects.filter( ~Q(id=request.user.id),Q(username__icontains=search_param)|Q(first_name__icontains=search_param))
    print(users)
    serializer=serializers.SearchUserSerializer(users,many=True)
    print(serializer.data)
    return Response(serializer.data)
    return Response('')

