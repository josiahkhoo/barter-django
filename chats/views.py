from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status, authentication, permissions

from .models import *
from .serializers import *
from .forms import *
from barter.utils import *
from chats.utils import *


# Create your views here.
class ChatView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        if not isinstance(request.user, User):
            return Response("Auth required",
                            status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        chat = get_object_or_404(Chat, pk=pk)
        if user not in chat.get_user_list():
            return Response("User not in chat",
                            status=status.HTTP_401_UNAUTHORIZED)
        # pass this context object into the serializer
        context = dict()
        oldest_message_id = request.GET.get("oldest_message_id")
        context["user"] = user
        if oldest_message_id:
            context["oldest_message_id"] = oldest_message_id
        body = serializer_to_body(
            ChatSerializer, chat, "chat", context=context
        )
        # # pagination is done here
        # if oldest_message_id:
        #     next_oldest_message = chat.messages.filter(
        #         pk__lt=oldest_message_id
        #     ).order_by('datetime_created')[:20].first()
        # else:
        #     next_oldest_message = chat.messages.order_by('datetime_created')[
        #         :20].first()
        # if next_oldest_message:
        #     next_oldest_message_id = next_oldest_message.id
        #     next_uri = "http://backend.staging.ruugi.com/api/chats/{}?oldest_message_id={}".format(
        #         chat.id, next_oldest_message_id)
        #     body["next_uri"] = next_uri
        # else:
        #     body["next_uri"] = None
        return Response(body, status=status.HTTP_200_OK)


class ChatMessageView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """
        This pk refers to the chat pk
        """
        if not isinstance(request.user, User):
            return Response("Auth required",
                            status=status.HTTP_401_UNAUTHORIZED)
        chat = get_object_or_404(Chat, pk=pk)
        user = request.user
        if user not in chat.get_user_list():
            return Response("User not in chat",
                            status=status.HTTP_401_UNAUTHORIZED)
        data = post_request_parser(request)
        data["chat"] = chat
        data["user"] = user
        data["message_type"] = int(MessageType.MESSAGE_USER)
        context = dict()
        # pass this context object into the serializer
        context["user"] = user
        form = MessageForm(data)
        if form.is_valid():
            message = form.save()
            data = serializer_to_body(
                ChatSerializer, chat, "chat", context=context
            )
            return Response(data, status.HTTP_200_OK)
        else:
            return Response(form.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserMessageView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """
        This pk refers to user pk
        """
        recipient_user = get_object_or_404(User, pk=pk)
        user = request.user
        data = post_request_parser(request)
        data["message_type"] = int(MessageType.MESSAGE_USER)
        data["recipient_user"] = recipient_user
        data["user"] = user
        context = dict()
        context["user"] = user
        form = MessageForm(data)
        if form.is_valid():
            message = form.save()
            data = serializer_to_body(
                MessageSerializer, message, "message", context=context
            )
            return Response(data, status.HTTP_200_OK)
        else:
            return Response(form.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ChatSeenView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        chat = get_object_or_404(Chat, pk=pk)
        receipt, created = Receipt.objects.get_or_create(
            chat=chat,
            user=request.user
        )
        receipt.save()
        # pass this context object into the serializer
        context = dict()
        oldest_message_id = request.GET.get("oldest_message_id")
        context["user"] = user
        if oldest_message_id:
            context["oldest_message_id"] = oldest_message_id
        body = serializer_to_body(
            ChatSerializer, chat, "chat", context=context
        )
        # pagination is done here
        if oldest_message_id:
            next_oldest_message = chat.messages.filter(
                pk__lt=oldest_message_id
            ).order_by('datetime_created')[:20].first()
        else:
            next_oldest_message = chat.messages.order_by('datetime_created')[
                :20].first()
        if next_oldest_message:
            next_oldest_message_id = next_oldest_message.id
            next_uri = "http://backend.staging.ruugi.com/api/chats/{}?oldest_message_id={}".format(
                chat.id, next_oldest_message_id)
            body["next_uri"] = next_uri
        else:
            body["next_uri"] = None
        return Response(body, status=status.HTTP_200_OK)
