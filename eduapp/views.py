from django.shortcuts import render, HttpResponse
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from .scrap import getVideos


# Create your views here

def index(request):
    if request.method == 'POST':
        videos = getVideos(request.POST['search_query'])
        return render(request, 'eduapp/index.html', {'videos': videos})
    return render(request, 'eduapp/index.html')


def player(request, video_url):
    return render(request, 'eduapp/player.html', {'video_url': video_url})


def react(request):
    return render(request, 'index.html')
