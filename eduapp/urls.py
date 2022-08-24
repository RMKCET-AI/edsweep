from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.index, name='index'),
    path('player/<str:video_url>', views.player, name='player'),
    path('<str:search_query>', views.results, name='results'),
    path('api/<str:search_query>',views.apiResults,name='api')
]

admin.site.site_header = "EDsweep"
admin.site.site_title = "Welcome to Edsweep dashboard"
admin.site.index_title = "Dashboard Edsweep"