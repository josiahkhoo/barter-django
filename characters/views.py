from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from barter.utils import serializer_to_body, post_request_parser

from .serializers import CharacterSerializer
from .models import Character
from .forms import CharacterForm
# Create your views here.


class CharacterView(APIView):

    def get(self, request, pk):
        try:
            character = Character.objects.get(pk=pk)
            body = serializer_to_body(
                CharacterSerializer, character, "character"
            )
            return Response(body, status=status.HTTP_200_OK)
        except Character.DoesNotExist:
            return Response("Character does not exist",
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = post_request_parser(request)
        form = CharacterForm(data)
        if form.is_valid():
            character = form.save()
            body = serializer_to_body(
                CharacterSerializer, character, "character"
            )
            return Response(body, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
