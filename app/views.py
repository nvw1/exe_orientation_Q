# author : Hao, Sam


from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.http import Http404
from app.models import Gamecode
from app.models import Questions

num = 1

def index(request):
    global num
    num = 1

    return render(request, 'app/index.html')

def redirect(request):
    global num
    if request.method == 'POST' and 'submit-groupcode' in request.POST:
        print("recieved post and submit-groupcode")
        print(request.POST)
        groupcode = str(request.POST.get('groupCode'))
        print(groupcode)
        print(Gamecode.objects.all())
        print("apparently that did work")

        print(Questions)
        print(Questions.objects.all())
        info = Questions.objects.filter(node_num=num)
        print(info)
        print("info got")


        if Gamecode.objects.filter(groupcode=groupcode).exists():
            print("groupcodes matched")
            request.session['groupcode'] = groupcode
            print("session request successful")
            print(id)
            return render(request, 'app/studentview.html',{"groupcode":groupcode, "data":info, "id":id})


        else:
            print("Wrong")
            messages.error(request, 'The game code does not exist')
            return render(request, 'app/index.html')

    if request.method == 'POST' and 'submit-question' in request.POST:
        groupcode = request.session['groupcode']
        data = str(request.POST.get('answer'))

        if Questions.objects.filter(answers=data, node_num=int(num)).exists():
            num += 1
            if Questions.objects.filter(node_num=int(num)).exists():
             info = Questions.objects.filter(node_num=num)
             messages.success(request, 'Correct!')
             return render(request, 'app/studentview.html',{"groupcode":groupcode,"data":info,"id":id})

            else:
                num -=1
                info = Questions.objects.filter(node_num=num)
                messages.success(request, 'You have finished the quiz, well done!')
                return render(request, 'app/studentview.html', {"groupcode": groupcode, "data": info, "id": id})
                
        else:
            info = Questions.objects.filter(node_num=num)
            messages.error(request, 'That is the wrong answer, please try again')
            return render(request, 'app/studentview.html', {"groupcode": groupcode, "data": info, "id": id})
    print(request.method)
    return HttpResponse()


def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def MVP_treasure_hunt(request):
	return render(request, 'app/MVP_treasure_hunt.html')

def studentview(request):
    return render(request,'app/studentview.html')
