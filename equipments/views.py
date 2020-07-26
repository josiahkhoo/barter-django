from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from barter.utils import serializer_to_body, post_request_parser, serializer_to_many_body
from .serializers import EquipmentSerializer
from .models import Equipment
from characters.serializers import *

# Create your views here.


class EquipmentView(APIView):

    def get(self, request, pk=None):
        user = request.user
        if request.GET.items():
            filters_dict = request.GET.dict()
            character_id = filters_dict.get('character_id')
            character = user.characters.get(pk=character_id)
            battles = character.battles.all()
            equipments = set(
                filter(lambda x: x, map(lambda x: x.equipment, battles)))
            equipment_type = filters_dict.get('equipment_type')
            if equipment_type:
                equipments = list(
                    filter(lambda x: x.equipment_type == int(equipment_type),
                           equipments))
            body = serializer_to_many_body(
                EquipmentSerializer, equipments, "equipments"
            )
            return Response(body, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        """
        Retrieves character id from form
        """
        user = request.user
        equipment = get_object_or_404(Equipment, pk=pk)
        data = post_request_parser(request)
        character_id = data.get('character_id', data)
        character = user.characters.get(pk=character_id)
        character = character.equip(equipment)
        body = serializer_to_body(
            CharacterSerializer, character, "character"
        )
        return Response(body, status=status.HTTP_200_OK)
