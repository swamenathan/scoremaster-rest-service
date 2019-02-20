from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import  permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
from rest_framework import generics
from gamesetmatch.serializers import *
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


class PlayerListView(APIView):
    """
    List All Players
    """
    authentication_classes = (JSONWebTokenAuthentication, )

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

    def get(self, request, main_player):
        team = get_object_or_404(Team, main_player=main_player)
        serializer = TeamSerializer(instance=team)
        return Response(serializer.data, status.HTTP_200_OK)


class TeamListView(APIView):

    authentication_classes = (JSONWebTokenAuthentication, )

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

    def get(self, request):
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchList(generics.ListAPIView):

    authentication_classes = (JSONWebTokenAuthentication, )

    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('team_1', 'team_2', )


class PlayerList(generics.ListAPIView):

    authentication_classes = (JSONWebTokenAuthentication, )

    queryset = PlayerProfile.objects.all()
    serializer_class = PlayerProfileSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('division', )


class ScoreDetailView(APIView):

    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request, match):
        score = get_object_or_404(Score, match=match)
        serializer = ScoreSerializer(instance=score, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScoreListView(APIView):

    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request):
        score = Score.objects.filter()
        serializer = ScoreSerializer(score, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)