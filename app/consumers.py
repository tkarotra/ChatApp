from channels.consumer import AsyncConsumer
from django.contrib.auth import get_user_model
import json
from channels.db import database_sync_to_async
from .models import *
from datetime import datetime

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connect', event)
        user_id = self.scope['session']['id']
        chat_room = f'user_chatroom_{user_id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })
        
    async def websocket_receive(self, event):
        print('receive', event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        sent_by_id = received_data.get('sent_by')
        sent_to_id = received_data.get('sent_to')
        room_id = received_data.get('room_id')
        if not msg:
            print('ERROR MESSAGE --> Empty Message')
            return False

        # sent_by_user = await self.get_user_object(sent_by_id)
        # if not sent_by_user:
        #     print("ERROR MESSAGE --> Sent By User Doesn't Exist")
        #     return False
        # sent_to_user = await self.get_user_object(sent_to_id)
        # if not sent_to_user:
        #     print("ERROR MESSAGE --> Sent To User Doesn't Exist")
        #     return False
        # room_obj = await self.get_room_object(room_id)
        # if not room_obj:
        #     print("ERROR MESSAGE --> Room Doesn't Exist")

        result = await self.add_message(room_id, sent_by_id, msg)
        if result == 'Error':
            return False

        other_user_chat_room = f'user_chatroom_{sent_to_id}'
        self_user_id = self.scope['session']['id']
        response = {
            'message': msg,
            'sent_by': self_user_id,
            'room_id': room_id
        }

        await self.channel_layer.group_send (
            other_user_chat_room, {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )
        await self.channel_layer.group_send (
            self.chat_room, {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )
        
    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def chat_message(self, event):
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })
    
    '''@database_sync_to_async
    def get_room_object(self, room_id):
        qs = ChatRoom.objects.filter(id=room_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    
    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj'''
        
    @database_sync_to_async
    def add_message(self, room_id, sent_by_id, msg):
        try:
            sent_by_user_obj = User.objects.get(id=sent_by_id)
        except Exception as e:
            print('ERROR MESSAGE ----------> ', e)
            return 'Error'
        try:
            room_obj = ChatRoom.objects.get(id=room_id)
        except Exception as e:
            print('ERROR MESSAGE ----------> ', e)
            return 'Error'
        try:
            qs = Message.objects.create(
                Room_ID = room_obj,
                Sent_By = sent_by_user_obj,
                Message_Text = msg,
                Sent_DateTime = datetime.now()
            )
            room_obj.LastMessageBy = sent_by_user_obj
            room_obj.MessageRead = False
            room_obj.Sent_DateTime = datetime.now()
            room_obj.save()
            return 'Success'
        except Exception as e:
            print('ERROR MESSAGE ----------> ', e)
            return 'Error'
        # room_qs = ChatRoom.objects.get(id=room_id)
        # room_qs.LastMessageBy = sent_by_id
        # room_qs.Sent_DateTime = datetime.now()