# author : Hao, Sam

from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.http import Http404
from app.models import Gamecode
from app.models import Questions
from app.models import *
import json
# current node number, global variable
num = 1
score = 0

def index(request):
    # sets the node num to 1 when landing on index page
    global num
    num = 1
    return render(request, 'app/index.html')


def redirect(request):
    global score
    global num
    map_check = False
    # Below is to check if whether the button is for groupcode or answer to question
    # process the group code passed from the landing page
    if request.method == 'POST' and 'submit-groupcode' in request.POST:
        groupcode = str(request.POST.get('groupCode'))    # Get inputted groupcode from the user
        # if the group code exists, load the treasure hunt page with the correct questions
        if Gamecode.objects.filter(groupcode=groupcode).exists():
            questionNum = Gamecode.objects.get(groupcode=groupcode)
            routeID = questionNum.routeID_id
            num = questionNum.questionNum
            print(Gamecode.objects.all())
            info = Questions.objects.filter(node_num=int(num),routeID=routeID)  # Get question from the database using num counter
            request.session['groupcode'] = groupcode         #Add group code into user's session
            request.session['score'] = score            #  Add score into user's session
            request.session['routeID'] = routeID
            return render(request, 'app/studentview.html',{"groupcode":groupcode, "data":info, "id":id, "score":score})
        else:
            print("Wrong")
            messages.error(request, 'The game code does not exist')
            return render(request, 'app/index.html')


    # if an answer to question is submitted, check if it is correct
    if request.method == 'POST' and 'submit-question' in request.POST:
        routeID = request.session['routeID']

        groupcode = request.session['groupcode']            #Get groupcode from user's sessio
        data = str(request.POST.get('answer'))              #Get text from the input answer box
        questionNum = Gamecode.objects.get(groupcode=groupcode)

        # if answer is correct for the current node, move onto the next question if it exists, 
        # otherwise show they have finished the quiz
        if Questions.objects.filter(answers__icontains=data.strip(), node_num=int(num), routeID=routeID).exists(): #Check if user get's the answer correct

            latest_question = Questions.objects.get(node_num=num, routeID=routeID)
            location = latest_question.location
            longtitude = latest_question.longtitude
            latitude = latest_question.latitude
            map_check = True
            num += 1  # Add 1 to the counter so the questions moves on to the next one
            if Questions.objects.filter(node_num=int(num), routeID=routeID).exists():     #Check whether if the user is on the last question
                score += 3
                questionNum.questionNum = num
                questionNum.save()
                print(location)
                info = Questions.objects.filter(node_num=num, routeID=routeID)
                messages.success(request, 'Correct!')  #Generate message saying correct
                return render(request, 'app/studentview.html',{"groupcode":groupcode,"data":info,"id":id,
                                                               "score":score, "map_check":map_check,
                                                               "location":location,"longtitude": longtitude,
                                                               "latitude":latitude})

            else:                 #Case when the user is on the last question
                num -= 1
                questionNum.questionNum = num
                questionNum.save()
                info = Questions.objects.filter(node_num=num, routeID=routeID)
                messages.success(request, 'You have finished the quiz, well done!')  #Generate message when user finish the quiz
                return render(request, 'app/studentview.html', {"groupcode": groupcode, "data": info, "id": id,"score":score})
        else:         # Case when user gets the answer wrong

            info = Questions.objects.filter(node_num=num, routeID=routeID)
            messages.error(request, 'That is the wrong answer, please try again')
            # Return incorrect message
            return render(request, 'app/studentview.html', {"groupcode": groupcode, "data": info, "id": id})
    if 'groupcode' in request.session:
        groupcode = request.session['groupcode']
        routeID = request.session['routeID']
        questionNum = Gamecode.objects.get(groupcode=groupcode)
        num = questionNum.questionNum
        info = Questions.objects.filter(node_num=int(num), routeID=routeID)  # Get question from the database using num counter
        return render(request, 'app/studentview.html', {"groupcode": groupcode, "data": info, "id": id,"score":score})
    else:
        num = 1
        return render(request, 'app/index.html')


def hint(request):
    global score           #Global score
    hint = Questions.objects.values_list('hints', flat=True).filter(node_num=num)
    score1 = request.POST.get('score')        #  Get score from ajax request
    request.session['score'] = score1      # update score variable
    score = int(score1)
    return HttpResponse(hint)


def update_request(request):
    question_num = request.POST.get('current_question')
    group_num = request.session['groupcode']
    latest_question = Gamecode.objects.get(groupcode=group_num)
    latest_num = latest_question.questionNum
    if int(question_num) != int(latest_num):
        return HttpResponse("Not the same")
    else:
        return HttpResponse("Same Question")


def reset_question(request):
    global num
    t = Gamecode.objects.get(groupcode='0001')
    t.questionNum = '1'
    t.save()
    num = 1



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


def faq(request):
    return render(request,'app/FAQ.html')


def contact(request):
    return render(request,'app/contact.html')


def game_master_page(request):
    route_list = Routes.objects.all()

    return render(request, 'app/game_master_page.html',{"route_list":route_list})


def create_route(request):
    routeId = request.POST.get('data2')
    routeName = request.POST.get('routeName')
    number = 0
    for i in range(len(routeId)):
        if routeId[i] == "=":
            number = i
    routeId= routeId[number+1::]

    print(Routes.objects.filter(routeID=int(routeId)).exists())
    if Routes.objects.filter(routeID=int(routeId)).exists():
        print("Yeah it does")
        return HttpResponse("Exist")
    else:
        print("No it does not ")
        c = Routes.objects.create(routeID = routeId, RouteName = routeName, gameMaster_GMID_id=1, Node = "1", NodeID= 1)
        c.save()
        c.refresh_from_db()
        print("Hello")
        return HttpResponse("Does not exist")


def add_question(request):

    question = request.POST.get('question')
    answer = request.POST.get('answer')
    hint = request.POST.get('hint')
    location = request.POST.get('location')
    latitude = request.POST.get('latitude')
    longtitude = request.POST.get('longtitude')
    node_num = request.POST.get('node_num')
    routeID = request.POST.get('routeID')
    routeID = striptext(routeID)
    print(question,answer,hint,location,latitude,longtitude,node_num,routeID)
    b = Questions()
    b.questions = question
    b.answers = answer
    b.hints = hint
    b.location = location
    b.latitude = float(latitude)
    b.longtitude = float(longtitude)
    b.node_num = int(node_num)
    b.routeID_id = int(routeID)
    b.save()
    if Questions.objects.filter(questions=question).exists():
        return HttpResponse("Added successfully")
    else:
        return HttpResponse("Not added")


def striptext(variable):
    number = 0
    for i in range(len(variable)):
        if variable[i] == "=":
            number = i
            break
    return variable[number+1::]


def removesign(variable):
    variable.replace("%"," ")
    return variable


def get_route(request):
    route_list = Routes.objects.all()
    for i in route_list.iterator():
        print(i)
    return HttpResponse({"route":route_list})



def create_game(request):
    groupcode1 = request.POST.get("groupcode")
    routeID = request.POST.get("routeID")
    if Gamecode.objects.filter(groupcode=groupcode1).exists():
        return HttpResponse("Exist")
    else:
        a = Gamecode()
        a.groupcode = groupcode1
        a.routeID_id= routeID
        a.save()
        return HttpResponse("Added")

