from .models import *
from rest_framework import viewsets, permissions
from .serializer import *


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = MailingSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ClientSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = MessageSerializer

