from django.shortcuts import render, HttpResponse
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from .scrap import getVideos
from django.core.paginator import Paginator


# Create your views here

def index(request):
    return render(request, 'eduapp/index.html')


def results(request, search_query):
    videos = sorted(getVideos(search_query, 20),key=lambda ele : ele.score,reverse= True)
    #video_scores = sorted([video.score for video in videos], reverse=True)
    #for index in range(len(videos)):
    #    videos[index].score = video_scores[index]
    paginator = Paginator(videos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'eduapp/index.html', {'page_obj': page_obj})


def player(request, video_url):
    return render(request, 'eduapp/player.html', {'video_url': video_url})


def react(request):
    return render(request, 'index.html')


def apiResults(request, search_query):
    videos = sorted(getVideos(search_query, 20),key= lambda ele : ele.score,reverse= True)
    # video_scores = sorted([video.score for video in videos], reverse=True)
    # for index in range(len(videos)):
    #    videos[index].score = video_scores[index]
    json_response = json.dumps([video.__dict__ for video in videos], indent=4)
    return HttpResponse(json_response, 'application/json charset=utf-8')
