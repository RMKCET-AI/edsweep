from django.shortcuts import render, HttpResponse
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from .scrap import getVideos
from django.core.paginator import Paginator
from .models import ContentFilter
from .web_scrap import getWebVideos
from .models import VideoCache,CustomVideo

allVideos = {}

# Create your views here

def index(request):
    return render(request, 'eduapp/index.html')


def results(request, search_query):
    if search_query not in allVideos:
        videos = sorted(getWebVideos(search_query, 20), key=lambda video: video.get_score(), reverse=True)
        allVideos[search_query] = videos
    else:
        print("Using cached results")
        videos = allVideos[search_query]
    paginator = Paginator(videos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'eduapp/index.html', {'page_obj': page_obj})


def player(request, video_url):
    return render(request, 'eduapp/player.html', {'video_url': video_url})


def apiResults(request, search_query):
    if search_query not in allVideos:
        videos = sorted(getWebVideos(search_query, 20), key=lambda video: video.get_score(), reverse=True)
        allVideos[search_query] = videos
    else:
        print("Using cached results")
        videos = allVideos[search_query]
    json_response = json.dumps([video.__dict__ for video in videos], indent=4)
    return HttpResponse(json_response, 'application/json charset=utf-8')

def custom_video(request):
    if request.method == 'POST':
        video = request.POST.get('video')
        CustomVideo.objects.create(video=video)

    return render(request, 'eduapp/upload.html')
