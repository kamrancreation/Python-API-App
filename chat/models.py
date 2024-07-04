from django.db import models

class ChatMessage(models.Model):
    client_message = models.TextField()
    response_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
