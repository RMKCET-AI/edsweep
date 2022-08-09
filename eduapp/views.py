from django.shortcuts import render,HttpResponse
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
# Create your views here.

def index(request):
    if request.method == 'POST':
        search_query = request.POST
        print(search_query['search_query'])
        return HttpResponse("Post request")
    return render(request, 'eduapp/index.html')


def react(request):
    return render(request, 'index.html')

