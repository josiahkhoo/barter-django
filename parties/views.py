from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework import status, authentication, permissions

from .serializers import *
from .forms import *

from users.models import *
from barter.utils import *
from characters.models import *
from parties.utils import *
# Create your views here.


class PartyView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, pk=None):
        if isinstance(request.user, User):
            user = request.user
            deal_id = request.GET.dict().get("deal_id", None)
            if pk:
                party = get_object_or_404(Party, pk=pk)
                if user not in party.users.all():
                    return Response("User is not part of this party",
                                    status=status.HTTP_400_BAD_REQUEST)
                body = serializer_to_body(
                    PartySerializer, party, "party", context={"user": user}
                )
                return Response(body, status=status.HTTP_200_OK)
            else:
                # filters for only post sale and ongoing parties
                parties = user.parties.all()
                body = serializer_to_many_body(
                    PartySerializer, parties, "parties", context={"user": user}
                )
                return Response(body, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # Adds current user into the party when he creates a party
        if not isinstance(request.user, User):
            return Response("Auth required",
                            status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        data = post_request_parser(request)
        form = PartyForm(data)
        if form.is_valid():
            party = form.save()
            party.users.add(user)
            # sets current user as the leader
            party.save()
            data = serializer_to_body(
                PartySerializer, party, "party", context={"user": user}
            )
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(form.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not isinstance(request.user, User):
            return Response("Auth required",
                            status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        party = get_object_or_404(Party, pk=pk)
        if user is party.leader:
            party.delete()
            return Response("Party deleted", status=status.HTTP_200_OK)
        else:
            return Response("User is not the party leader, unable to delete",
                            status=status.HTTP_401_UNAUTHORIZED)


class PartyJoinView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, access_code):
        """
        Takes in a access_code and makes current user join the party
        form data required:
        """
        if not isinstance(request.user, User):
            return Response("Auth required",
                            status=status.HTTP_401_UNAUTHORIZED)
        if not access_code:
            return Response("No access code specified",
                            status=status.HTTP_400_BAD_REQUEST)
        print(access_code)
        party = get_object_or_404(Party, access_code=access_code)
        if party.state == int(PartyState.COMPLETED):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        party.add_user(user)
        data = serializer_to_body(
            PartySerializer, party, "party",
        )
        return Response(data, status.HTTP_200_OK)


class PartyLeaveView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        """
        Takes in a pk and makes current user leave the party
        """
        if not isinstance(request.user, User):
            return Response("Auth required",
                            status=status.HTTP_401_UNAUTHORIZED)
        party = get_object_or_404(Party, pk)
        user = request.user
        if user == party.leader:
            return Response("User is the party leader, unable to leave",
                            status=status.HTTP_400_BAD_REQUEST)
        if user not in party.users.all():
            return Response("User is not part of this party",
                            status=status.HTTP_400_BAD_REQUEST)
        party.remove_user(user)
        data = serializer_to_body(
            PartySerializer, party, "party", context={"user": user}
        )
        return Response(data, status.HTTP_200_OK)


class PartyKickView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """
        Takes in a party pk and kicks user specified in form data
        """
        if not isinstance(request.user, User):
            return Response("Auth required",
                            status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        party = get_object_or_404(Party, pk=pk)
        data = post_request_parser(request)
        if user != party.leader:
            return Response("User is not the party leader, unable to delete",
                            status=status.HTTP_401_UNAUTHORIZED)
        other_user_id = data.get("user", None)
        other_user = get_object_or_404(User, pk=other_user_id)
        if not other_user:
            return Response("No user specified",
                            status=status.HTTP_400_BAD_REQUEST)
        elif other_user is user:
            return Response("Cannot kick yourself",
                            status=status.HTTP_400_BAD_REQUEST)
        party.kick_user(other_user)
        data = serializer_to_body(
            PartySerializer, party, "party", context={"user": user})
        return Response(data, status.HTTP_200_OK)


class PartyPollView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, access_code):
        """
        Takes in a e.g.
        status:
        [0] - not ready
        [1] - ready
        """
        user = request.user
        party = get_object_or_404(Party, access_code=access_code)
        data = post_request_parser(request)
        state = data.get("state", None)
        character_id = data.get("character", None)
        character = Character.objects.get(pk=character_id)
        if not state:
            return Response("No status", status=status.HTTP_400_BAD_REQUEST)
        result = party.poll(user, character, state)
        ready_characters = result["ready_characters"]
        all_characters = result["all_characters"]
        all_ready = result["all_ready"]
        return Response({
            "data": {
                "ready_characters": CharacterSerializer(ready_characters,
                                                        many=True).data,
                "all_characters": CharacterSerializer(all_characters,
                                                      many=True).data,
                "all_ready": all_ready
            }
        }, status=status.HTTP_200_OK)
