from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request,"eduapp/index.html")


def react(request):
    return render(request, 'index.html')

