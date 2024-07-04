import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        client_message = text_data_json['message']

        # Dummy response
        response_message = "This is a dummy response."

        # Save messages to the database
        chat_message = ChatMessage(client_message=client_message, response_message=response_message)
        chat_message.save()

        await self.send(text_data=json.dumps({
            'message': response_message
        }))
