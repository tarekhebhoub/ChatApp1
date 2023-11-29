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
import ast
from . import models
# Create your views here.

def hello(request):
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

        # request.data['ouserswner']=user.id
        # request.data['users']=[user.id]
        # serializer = serializers.RoomSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data,status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=400)
    def get(self,request):
        user=request.user

# Get rooms where the user is a member
        rooms = models.Room.objects.filter(Q(users=user)|Q(owner=user))
        print(rooms)
        # rooms=models.Room.objects.filter(users=user.id)
        serializer=serializers.RoomSerializer(rooms,many=True)
        data=serializer.data
        i=0
        for room in rooms:
            full_users_list = list(get_user_model().objects.filter(id__in=room.users.all()))
            userSerializer=serializers.UserSerializer(full_users_list,many=True)
            ownerSerializer=serializers.UserSerializer(room.owner)
            data[i]['owner']=ownerSerializer.data
            room_messages = models.Message.objects.filter(room=room.id).order_by('-timestamp')
            if room_messages.exists():
                last_message_in_room = room_messages.first()
                messageSerializer=serializers.MessageSerializer(last_message_in_room)
                data[i]['latestMessage']=messageSerializer.data
                # Now, last_message_in_room contains the last message in the specified room
            else:
                # Handle the case when there are no messages in the specified room
                data[i]['latestMessage']=None

            data[i]['users']=userSerializer.data
            i+=1
        return Response(data)

class MessageView(APIView):
    def post(self,request,id_room):
        data=request.data
        rooms=models.Room.objects.get(id=id_room)
        data['sender']=request.user.id
        data['room']=id_room
        serializer=serializers.MessageSerializer(data=data)
        if serializer.is_valid():

            serializer.save()
            data=serializer.data
            data['sender']=request.user.id
            user=serializers.UserSerializer(request.user)
            data['sender']=user.data
            room=serializers.RoomSerializer(rooms)
            room=room.data
            users=room['users']
            listUsers=[]
            for idUser in users:
                user=models.User.objects.get(id=idUser)
                userSerializer=serializers.UserSerializer(user)
                listUsers.append(userSerializer.data)
            room['users']=listUsers
            data['room']=room

            data['room']=room

            if data['readBy']:
                readBy=serializers.UserSerializer(data['readBy'])
                data['readBy']=readBy.data
            return Response(data)
        return Response(serializer.errors)
    def get(self,request,id_room):
        # room=models.objects.get(id=id_room)
        messages=models.Message.objects.filter(room=id_room)
        serializer=serializers.MessageSerializer(messages,many=True)
        data=serializer.data
        i=0
        for message in messages:
            user=serializers.UserSerializer(message.sender)
            data[i]['sender']=user.data
            room=serializers.RoomSerializer(message.room)
            room=room.data

            users=room['users']
            listUsers=[]
            for idUser in users:
                user=models.User.objects.get(id=idUser)
                userSerializer=serializers.UserSerializer(user)
                listUsers.append(userSerializer.data)
            room['users']=listUsers
            data[i]['room']=room
            if message.readBy:
                readBy=serializers.UserSerializer(message.readBy)
                data[i]['readBy']=readBy.data
            i+=1
        return Response(data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tryToken(request):
    return Response({'tarek'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchUsers(request):
    search_param = request.GET.get('search', '')

    users=models.User.objects.filter( ~Q(id=request.user.id),Q(username__icontains=search_param)|Q(first_name__icontains=search_param))
    serializer=serializers.SearchUserSerializer(users,many=True)
    return Response(serializer.data)
    return Response('')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createGroupe(request):
    print(request.data)



    data1=request.data
    roomData={}
    roomData["owner"]=request.user
    roomData["name_room"]=data1["name"]
    users=data1['users'] 
    roomData['isGroupeChat']=True
    users = ast.literal_eval(users)

    room=models.Room.objects.create(**roomData)
    room.users.set(users)
    serializer=serializers.RoomSerializer(room)
    data=serializer.data
    full_users_list = list(get_user_model().objects.filter(id__in=users))
    userSerializer=serializers.UserSerializer(full_users_list,many=True)
    data['users']=userSerializer.data
    return Response(data)