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

def results(request,search_query):
    videos = sorted(getVideos(search_query,20),key=lambda x: x.score,reverse=True)
    paginator = Paginator(videos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'eduapp/index.html', {'page_obj': page_obj})


def player(request, video_url):
    return render(request, 'eduapp/player.html', {'video_url': video_url})


def react(request):
    return render(request, 'index.html')
