from rest_framework.status import HTTP_200_OK
from barter.utils import serializer_to_many_body
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status, authentication, permissions

from .serializers import *
from .forms import *
from barter.utils import *
# Create your views here.


class BattleView(APIView):
    """
    Pass Character ID
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        """
        api/battles?character_id=x
        """
        user = request.user
        if pk:
            battle = get_object_or_404(Battle, pk=pk)
            if battle.character.user == user:
                body = serializer_to_body(
                    BattleSerializer, battle, "battle", context={"user": user}
                )
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            query_params = request.GET.dict()
            if query_params:
                character_id = query_params.get("character_id")
                battles = user.characters.get(pk=character_id).battles
                body = serializer_to_many_body(
                    BattleSerializer, battles, "battles",
                    context={"user": user}
                )
                return Response(body, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        """
        form data
        character = x
        """
        user = request.user
        data = post_request_parser(request)
        data["character"] = user.characters.get(pk=data["character"])
        form = BattleForm(data)
        if form.is_valid():
            battle = form.save()
            data = serializer_to_body(
                BattleSerializer, battle, "battle", context={"user": user}
            )
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class BattleCompleteView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        battle = get_object_or_404(Battle, pk=pk)
        if battle.character.user != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        battle.set_state_complete()
        data = serializer_to_body(
            BattleSerializer, battle, "battle", context={"user": user}
        )
        return Response(data, status=status.HTTP_200_OK)


class BattleForfeitView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        battle = get_object_or_404(Battle, pk=pk)
        if battle.character.user != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        battle.set_state_forfeited()
        data = serializer_to_body(
            BattleSerializer, battle, "battle", context={"user": user}
        )
        return Response(data, status=status.HTTP_200_OK)
