from django.shortcuts import get_object_or_404
from .models import Mailing, Client, Message
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializer import MailingSerializer, ClientSerializer, MessageSerializer
from rest_framework.decorators import action


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = MailingSerializer

    @action(detail=False, methods=["get"])
    def list_mailings(self, request):
        queryset = Mailing.objects.all()
        serializer = MailingSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def retrieve_mailings(self, request, pk=None):
        queryset = Mailing.objects.all()
        mailing = get_object_or_404(queryset, pk=pk)
        serializer = MailingSerializer(mailing)
        return Response(serializer.data)


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


