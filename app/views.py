from __future__ import unicode_literals
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.http import Http404
from django.shortcuts import render
from app.models import Gamecode


def index(request):
    return render(request, 'index.html')

def redirect(request):
    if request.method == 'POST':
        data = str(request.POST.get('groupCode'))
        print(Gamecode.objects.all())
        if Gamecode.objects.filter(groupcode=data).exists():

            return render(request, 'redirect.html')
        else:
            print("Wrong")
            messages.error(request, 'The game code does not exist')
            return render(request, 'index.html')
    print(request.method)



def health(request):
    state = {"status": "UP"}
    return JsonResponse(state)


def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def gamemaster(request):
    return render(request,'gamemaster.html')