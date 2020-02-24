# author : Hao

from __future__ import unicode_literals
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.http import Http404
from django.shortcuts import render
from app.models import Gamecode
from app.models import Questions

num = 1

def index(request):
    global num
    num = 1

    return render(request, 'index.html')

def redirect(request):
    global num
    if request.method == 'POST' and 'submit-groupcode' in request.POST:
        groupcode = str(request.POST.get('groupCode'))
        print(Gamecode.objects.all())
        info = Questions.objects.filter(auto_increment_id=num)
        if Gamecode.objects.filter(groupcode=groupcode).exists():
            request.session['groupcode'] = groupcode
            return render(request, 'studentview.html.',{"groupcode":groupcode, "data":info,"id":id})
        else:
            print("Wrong")
            messages.error(request, 'The game code does not exist')
            return render(request, 'index.html')
    if request.method == 'POST' and 'submit-question' in request.POST:
        groupcode = request.session['groupcode']
        data = str(request.POST.get('answer'))
        if Questions.objects.filter(answers=data, auto_increment_id=int(num)).exists():
            num += 1
            if Questions.objects.filter(auto_increment_id=int(num)).exists():
             info = Questions.objects.filter(auto_increment_id=num)
             messages.success(request, 'Correct!')
             return render(request, 'studentview.html.',{"groupcode":groupcode,"data":info,"id":id})
            else:
                num -=1
                info = Questions.objects.filter(auto_increment_id=num)
                messages.success(request, 'You have finished the quiz, well done!')
                return render(request, 'studentview.html.', {"groupcode": groupcode, "data": info, "id": id})
        else:
            info = Questions.objects.filter(auto_increment_id=num)
            messages.error(request, 'That is the wrong answer, please try again')
            return render(request, 'studentview.html.', {"groupcode": groupcode, "data": info, "id": id})
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

def studentview(request):
    return render(request,'studentview.html')
