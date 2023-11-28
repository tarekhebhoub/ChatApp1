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
        # self.room_group_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name='sender'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        input_string=text_data
        comma_index = input_string.index(',')

# Extract "chat" and the JSON object based on the comma index
        chat_part = text_data[:comma_index]

        text_data = text_data.split(',')
        print(text_data)
        if text_data[0]=='typing':
            print(text_data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'typing_notification',
                    'message':text_data[1],
                    'username':text_data[2],
                    'roomId':text_data[3]

                }
            )
        if text_data[0]=='chat':
            json_object_part = input_string[comma_index + 1:]

            print("tarek",json_object_part)
            # Extract the second element and join the components into a valid JSON string
            # Load the JSON string into a Python dictionary
            # json_string = json_string.replace('" "', '","')

            # json_object = json.loads(json_string)

            # msg = json.loads(text_data[1])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'chat_message',
                    'content':json_object_part
                }
            )
    async def chat_message(self,event):
        # print('tarek')
        await self.send(text_data=json.dumps({
            'type':'chat',
            'content':event["content"]
        }))

    async def typing_notification(self, event):
        # Send typing notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'is_typing': event['message'],
            'username':event['username'],
            'roomId':event['roomId']
        }))
    
# class TypingConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_group_name = self.scope['url_route']['kwargs']['room_name']
      
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()
#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         text_data = text_data.split(',')
#         print("typing",text_data)

#         # text_data_json = json.loads(text_data)
#         # action = text_data_json['action']
#         # username = text_data_json['username']

#         # if action == 'start_typing':
#             # await self.send_typing_notification(True)
#         # elif action == 'stop_typing':
#             # await self.send_typing_notification( False)

#         await self.send_typing_notification(text_data[0],text_data[1])
#     async def send_typing_notification(self, is_typing,username):
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': is_typing,
#                 'username':username
#             }
#         )

#     async def chat_message(self, event):
#         # Send typing notification to WebSocket
#         await self.send(text_data=json.dumps({
#             # 'action': 'typing_notification',
#             'is_typing': event['message'],
#             'username':event['username']
#         }))
#     