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
    global num       #  Allow variable to be accessed outside the definition
    num = 1
    return render(request, 'index.html')


def redirect(request):
    global num       #  Allow variable to be accessed outside the definition
    # Below is to check if whether the button is for groupcode or answer to question
    if request.method == 'POST' and 'submit-groupcode' in request.POST:
        groupcode = str(request.POST.get('groupCode'))    # Get inputted groupcode from the user
        print(Gamecode.objects.all())
        info = Questions.objects.filter(node_num=int(num))    # Get question from the database using num counter
        if Gamecode.objects.filter(groupcode=groupcode).exists():  #Check if the group code actually exists
            request.session['groupcode'] = groupcode               #Add group code into user's session
            return render(request, 'studentview.html.',{"groupcode":groupcode, "data":info,"id":id})
        else:                        #Case for when the invalid group code is entered
            print("Wrong")
            messages.error(request, 'The game code does not exist')
            return render(request, 'index.html')
    # Below is to check if whether the button is for groupcode or answer to question
    if request.method == 'POST' and 'submit-question' in request.POST:
        groupcode = request.session['groupcode']         #Get groupcode from user's session
        data = str(request.POST.get('answer'))        #Get text from the input answer box
        if Questions.objects.filter(answers__icontains=data.strip(), node_num=int(num)).exists(): #Check if user get's the answer correct
            num += 1       # Add 1 to the counter so the questions moves on to the next one
            if Questions.objects.filter(node_num=int(num)).exists():     #Check whether if the user is on the last question
             info = Questions.objects.filter(node_num=num)
             messages.success(request, 'Correct!')  #Generate message saying correct
             return render(request, 'studentview.html.',{"groupcode":groupcode,"data":info,"id":id})
            else:                 #Case when the user is on the last question
                num -=1      #Question stays the same when user has reach the end
                info = Questions.objects.filter(node_num=num)
                messages.success(request, 'You have finished the quiz, well done!')  #Generate message when user finish the quiz
                return render(request, 'studentview.html.', {"groupcode": groupcode, "data": info, "id": id})
        else:         #Case when user gets the answer wrong
            info = Questions.objects.filter(node_num=num)
            messages.error(request, 'That is the wrong answer, please try again')
            return render(request, 'studentview.html.', {"groupcode": groupcode, "data": info, "id": id}) #Return incorrect message
    print(request.method)


def hint(request):
    hint_get = Questions.objects.values_list('hints',flat=True).filter(node_num=num)
    print(hint_get)
    return HttpResponse(hint_get)


def health(request):
    state = {"status": "UP"}
    return JsonResponse(state)


def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def MVP_treasure_hunt(request):
	return render(request, 'app/MVP_treasure_hunt.html')

def studentview(request):
    return render(request,'app/studentview.html')
