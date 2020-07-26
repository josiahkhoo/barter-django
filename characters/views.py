from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from barter.utils import serializer_to_body, post_request_parser

from .serializers import CharacterSerializer
from .models import Character
from .forms import CharacterForm
from battles.utils import *
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


class CharacterAchievementView(APIView):
    def get(self, request, pk):
        try:
            character = Character.objects.get(pk=pk)
            battles = character.battles.all()
            total_count = battles.count()
            battles_won = battles.filter(state=BattleState.COMPLETED).count()
            battles_lost = total_count - battles_won
            total_success_time = sum(
                map(lambda x: x.monster.duration, battles.filter(
                    state=BattleState.COMPLETED)))
            body = [
                {
                    "name": "Total Battles",
                    "value": total_count
                },
                {
                    "name": "Battles Won",
                    "value": battles_won
                },
                {
                    "name": "Battles Lost",
                    "value": battles_lost
                },
                {
                    "name": "Total Success Time",
                    "value": "{} minutes".format(int(total_success_time / 60))
                }
            ]
            return Response(body, status=status.HTTP_200_OK)
        except Character.DoesNotExist:
            return Response("Character does not exist",
                            status=status.HTTP_400_BAD_REQUEST)
