import uuid
import json
# from .services.email_verification.service import EmailVerificationService
from .backends import JWTAuthentication
from .renderers import UserJSONRenderer
from .models import User
from .serializers import *
from .forms import *
from .utils import UserStatus
from barter.utils import *
from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render


# Create your views here.


class UserLoginView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = post_request_parser(request)
        print(data)
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            body = {'token': user.token}
            body.update(serializer_to_body(
                UserSerializer, user, "user"))
            # Redirect to a success page.
            return Response(body, status=status.HTTP_200_OK)
        else:
            # Return an 'invalid login' error message.
            return Response(
                "Invalid login, please check your username and password",
                status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    '''
    This is necessary in order to accept JSON Web Tokens
    POST Requests needs to have this in header:
    Key = Authorization
    Value = Token "Insert Token here"

    In order to access user from the request, do 'request.user'
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user.datetime_last_logout = timezone.now()
            user.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserCreateView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]
    Serializer = UserSerializer

    def post(self, request):
        data = post_request_parser(request)
        form = CustomUserCreationForm(data)
        if form.is_valid():
            user = form.save()
            body = serializer_to_body(self.Serializer, user, "user")
            # EmailVerificationService().send_email_verification(user)
            return Response(body, status=status.HTTP_200_OK)
        else:
            print(form.errors)
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]
    serializer_classes = [UserSerializer,
                          PublicUserSerializer, UserUpdateSerializer]

    def get(self, request, pk=None):
        try:
            if pk is None and not isinstance(request.user, AnonymousUser):
                user = request.user
                body = serializer_to_body(
                    UserSerializer, user, "user")
                return Response(body, status=status.HTTP_200_OK)

            elif pk:
                user = User.objects.get(pk=pk)
                body = serializer_to_body(
                    PublicUserSerializer, user, "user")
                return Response(body, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user
        serializer = UserUpdateSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            body = serializer_to_body(UserSerializer, user, "user")
            return Response(body, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class UserPasswordChangeView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        data = post_request_parser(request)
        # checks if password is set or is valid
        if user.has_usable_password():
            form = CustomPasswordChangeForm(user=user, data=data)
        else:
            form = CustomPasswordSetForm(user=user, data=data)
        if form.is_valid():
            user = form.save()
            body = serializer_to_body(UserSerializer, user, "user")
            return Response(body, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFriendsRequestView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        users = user.get_incoming_friend_requests()
        body = serializer_to_many_body(UserSerializer, users, "users")
        return Response(body, status=status.HTTP_200_OK)


class UserFriendsView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        users = user.get_friends()
        body = serializer_to_many_body(UserSerializer, users, "users")
        return Response(body, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """
        Initiate friend request or accept friend request using this view
        """
        user = request.user
        other_user = get_object_or_404(User, pk=pk)
        user.add_friend(other_user)
        users = user.get_friends()
        body = serializer_to_many_body(UserSerializer, users, "users")
        return Response(body, status=status.HTTP_200_OK)
