"""scoremanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from gamesetmatch.views import *

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    # path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('players/', PlayerListView.as_view()),
    path('players/<int:pk>', PlayerDetailView.as_view()),
    path('teams/', TeamListView.as_view()),
    path('matches/', MatchListView.as_view()),
    path('tours/', TournamentListView.as_view()),
    path('match/', MatchList.as_view()),
    path('divplayers/', PlayerList.as_view()),
    path('team/<int:main_player>', TeamDetailView.as_view()),
]
