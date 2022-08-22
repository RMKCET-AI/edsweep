from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('react', views.react, name='react'),
    path('player/<str:video_url>', views.player, name='player')
]
