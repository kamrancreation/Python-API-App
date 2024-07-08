from rest_framework import viewsets
from .serializers import ChatMessageSerializer
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatMessage
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatMessage
import json

# Initial bot message and symptoms
initial_bot_message = "How are you feeling, ma'am?"
symptoms_list = ["Do you also feel nausea?", "Do you have a fever?", "Are you experiencing dizziness?"]
diagnosis = "Based on your symptoms, you might have the flu. Please consult a doctor for a proper diagnosis."

# To store the conversation state
conversation_state = {}

@api_view(['POST'])
def send_message(request):
    user_id = request.data.get('user_id')
    client_message = request.data.get('message', '')

    if user_id not in conversation_state:
        conversation_state[user_id] = {
            "step": 1,
            "symptoms_confirmed": {}
        }
        response_message = initial_bot_message
        chat_message = ChatMessage(client_message=client_message, response_message=response_message)
        chat_message.save()
    else:
        state = conversation_state[user_id]
        step = state["step"]
        symptoms_confirmed = state["symptoms_confirmed"]

        if step == 1:
            # User replied to the initial message, move to the next step
            state["step"] = 2
            response_message = "Please reply with 'yes' or 'no' for the following symptoms: " + ", ".join(symptoms_list)
            chat_message = ChatMessage(client_message=client_message, response_message=response_message)
            chat_message.save()
        elif step == 2:
            if isinstance(client_message, dict) and all(symptom in client_message for symptom in symptoms_list):
                symptoms_confirmed = {symptom: client_message.get(symptom, "no") for symptom in symptoms_list}
                state["symptoms_confirmed"] = symptoms_confirmed
                state["step"] = 3
                response_message = diagnosis
            else:
                response_message = "Please provide a dictionary with your responses to each symptom."
            chat_message = ChatMessage(client_message=str(client_message), response_message=response_message)
            chat_message.save()
        else:
            response_message = "Thank you for using the bot. Stay healthy!"

    return Response({'message': response_message})

# Create your views here.
