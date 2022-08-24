from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('react', views.react, name='react'),
    path('player/<str:video_url>', views.player, name='player'),
    path('<str:search_query>',views.results,name='results'),
    path('api/<str:search_query>',views.apiResults,name='apiResults')
]
