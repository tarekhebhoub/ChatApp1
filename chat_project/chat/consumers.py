import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Message,Room
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']
      
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print(text_data)
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        # Broadcast the message to all connected clients
        # await self.send(text_data=json.dumps({'message': text_data}))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':text_data,
            }
        )
    async def chat_message(self,event):
        message=event["message"]
        # print('tarek')
        await self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
        }))
    
class TypingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']
      
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data = text_data.split(',')

        # text_data_json = json.loads(text_data)
        # action = text_data_json['action']
        # username = text_data_json['username']

        # if action == 'start_typing':
            # await self.send_typing_notification(True)
        # elif action == 'stop_typing':
            # await self.send_typing_notification( False)

        await self.send_typing_notification(text_data[0],text_data[1])
    async def send_typing_notification(self, is_typing,username):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_notification',
                'is_typing': is_typing,
                'username':username
            }
        )

    async def typing_notification(self, event):
        # Send typing notification to WebSocket
        await self.send(text_data=json.dumps({
            # 'action': 'typing_notification',
            'is_typing': event['is_typing'],
            'username':event['username']
        }))
    