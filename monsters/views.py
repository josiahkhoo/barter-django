from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from barter.utils import serializer_to_body, post_request_parser

from .serializers import MonsterSerializer
from .models import Monster
from .forms import MonsterForm
# Create your views here.


class MonsterView(APIView):

    def get(self, request, pk=None):
        """
        Retrieves single party bosses
        """
        if pk:
            try:
                monster = Monster.objects.get(pk=pk)
                body = serializer_to_body(
                    MonsterSerializer, monster, "monster"
                )
                return Response(body, status=status.HTTP_200_OK)
            except Monster.DoesNotExist:
                return Response("Monster does not exist",
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            monsters = Monster.objects.filter(
                party_size=1).order_by('pk').all()
            body = {"data": MonsterSerializer(monsters, many=True).data}
            return Response(body, status=status.HTTP_200_OK)

    def post(self, request):
        data = post_request_parser(request)
        form = MonsterForm(data)
        if form.is_valid():
            monster = form.save()
            body = serializer_to_body(
                MonsterSerializer, monster, "monster"
            )
            return Response(body, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            monster = Monster.objects.get(pk=pk)
            serializer = MonsterSerializer(
                monster, data=request.data, partial=True
            )
            if serializer.is_valid():
                monster = serializer.save()
                body = serializer_to_body(
                    MonsterSerializer, monster, "monster"
                )
                return Response(body, status=status.HTTP_200_OK)
            else:
                return Response("Invalid form",
                                status=status.HTTP_400_BAD_REQUEST)
        except Monster.DoesNotExist:
            return Response("Monster does not exist",
                            status=status.HTTP_400_BAD_REQUEST)


class MonsterMultiplayerView(APIView):

    def get(self, request, pk=None):
        """
        Retrieves multiplayer bosses
        """
        if pk:
            try:
                monster = Monster.objects.get(pk=pk)
                body = serializer_to_body(
                    MonsterSerializer, monster, "monster"
                )
                return Response(body, status=status.HTTP_200_OK)
            except Monster.DoesNotExist:
                return Response("Monster does not exist",
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            monsters = Monster.objects.filter(
                party_size__gte=2).order_by('pk').all()
            body = {"data": MonsterSerializer(monsters, many=True).data}
            return Response(body, status=status.HTTP_200_OK)
