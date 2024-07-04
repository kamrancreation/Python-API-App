from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatMessageViewSet, send_message

router = DefaultRouter()
router.register(r'messages', ChatMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send_message/', send_message, name='send_message'),
]
