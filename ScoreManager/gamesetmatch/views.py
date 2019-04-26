from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import  permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
from rest_framework import generics
from gamesetmatch.serializers import *
from gamesetmatch.permissions import *
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

class PlayerListView(APIView):
    """
    List All Players
    """
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (VerifiedPermission, )

    def get(self, request, format=None):
        players = settings.AUTH_USER_MODEL.objects.all()
        serializer = RegisterSerializer(players, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PlayerProfileSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerDetailView(APIView):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (VerifiedPermission, )

    def get(self, request, pk):
        playerprofile = get_object_or_404(PlayerProfile, pk=pk, player=request.user)
        serializer = PlayerProfileSerializer(instance=playerprofile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        playerprofile = get_object_or_404(PlayerProfile, pk=pk, player=request.user)
        serializer = PlayerProfileSerializer(instance=playerprofile, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        playerpofile = get_object_or_404(PlayerProfile, pk=pk, player=request.user)
        playerpofile.delete()
        return Response(status=status.HTTP_200_OK)


class TeamDetailView(APIView):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (VerifiedPermission, )

    def get(self, request, main_player):
        # team = get_object_or_404(Team, main_player=main_player)
        team = Team.objects.filter(Q(main_player=main_player) | Q(partner_player=main_player))
        if len(team) > 1:
            message = {"message": "A player is present in more than one team"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        serializer = TeamSerializer(instance=team[0])

        return Response(serializer.data, status.HTTP_200_OK)


class TeamListView(APIView):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (VerifiedPermission, )

    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TeamSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchListView(APIView):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (VerifiedPermission, )

    def get(self, request):
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MatchSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchList(APIView):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (VerifiedPermission, )

    def get(self, request):
        query_params = list(request.query_params.values())

        # print('list 1 = ', str(query_params))

        while 'undefined' in query_params:
            query_params.remove('undefined')

        # print('list 2 = ', str(query_params))

        if len(query_params) > 1:
            matches = Match.objects.filter(Q(team_1=query_params[0]) & Q(team_2=query_params[1]) | Q(team_1=query_params[1]) & Q(team_2=query_params[0]))
        elif len(query_params) == 1:
            matches = Match.objects.filter(Q(team_1=query_params[0]) | Q(team_2=query_params[0]))
        else:
            matches = Match.objects.all()

        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # serializer_class = MatchSerializer
        # filter_backends = (DjangoFilterBackend, )
        # filter_fields = ('team_1', 'team_2', 'match_type')


class PlayerList(generics.ListAPIView):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (VerifiedPermission, )


    queryset = PlayerProfile.objects.all()
    serializer_class = PlayerProfileSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('division', )


class TournamentListView(APIView):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (VerifiedPermission, )

    def get(self, request):
        tours = Tournament.objects.all()
        print('tours = ', tours)
        serializer = TournamentSerializer(tours, many=True)
        return Response(serializer.data)
