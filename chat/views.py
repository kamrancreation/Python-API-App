from rest_framework import viewsets
from .serializers import ChatMessageSerializer
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatMessage
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer


responses = [
    "This is a dummy response.",
    "Hello, how can I help you?",
    "Thank you for your message.",
    "I am here to assist you.",
    "What can I do for you today?"
]


@api_view(['POST'])
def send_message(request):
    client_message = request.data.get('message', '')
    response_message = random.choice(responses)
    chat_message = ChatMessage(client_message=client_message, response_message=response_message)
    chat_message.save()

    return Response({'message': response_message})

# Create your views here.
