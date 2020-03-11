# author : Hao, Sam

from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
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


@login_required(redirect_field_name='')  
def game_master_page(request):
    route_list = Routes.objects.all()
    questions = Questions.objects.all()
    return render(request, 'app/game_master_page.html',{"route_list":route_list,"questions":questions})

def login_page(request):
    return render(request, 'app/login_page.html')

def login_view(request):
    # if sign up button pressed
    if request.method == 'POST' and 'submit-signUp' in request.POST:
        newUsername = request.POST['username']
        newPassword = request.POST['password']

        # if the user does not already exist
        # set new user
        print("making new user")
        # if they are a superuser
        if 'superuser' in request.POST:
            newUser = User.objects.create_user(username=newUsername, password=newPassword, is_superuser=True)
        else:
            newUser = User.objects.create_user(username=newUsername, password=newPassword, is_superuser=False)
 
        # save the user in the database
        newUser.save()

        messages.success(request, 'Successfully made new user')
        return render(request, 'app/game_master_page.html')

        # else:
        #     print("User already exists")
        #     messages.error(request, 'Username already exists')
        #     return render(request, 'app/game_master_page.html')

    # if the submit button is pressed
    if request.method == 'POST' and 'submit-logIn' in request.POST:
        username = request.POST['username']
        password = request.POST['password']

        # authenticate that the username and password are correct
        user = authenticate(username=username, password=password)

        # if the user exists
        if user is not None:
            # log them in
            login(request, user)
            print("logged in")
            messages.success(request, 'log in success')
            return render(request, 'app/game_master_page.html')
        else:
            # report error
            print("log in failure")
            messages.error(request, 'log in failure')
            return render(request, 'app/login_page.html')

    # if the change password button is pressed
    if request.method == 'POST' and 'submit-changePass' in request.POST:
        # oldPass = request.POST['oldPass']
        # retreive the data
        newPass = request.POST['newPass']
        valPass = request.POST['valPass']

        # retrieve the current user
        user = request.user

        if user is not None:
            # check the passwords match
            if newPass == valPass:
                # set the new password and save to database
                user.set_password(newPass)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'password changed')
                return render(request, 'app/game_master_page.html')
            else:
                messages.error(request, 'passwords did not match')
                return render(request, 'app/game_master_page.html')
        else:
            # report errors
            print("log in failure")
            messages.error(request, 'log in failure')
            return render(request, 'app/login_page.html')

    print("did not get username or password")
    messages.error(request, 'did not get username or password')
    return render(request, 'app/login_page.html')

# log the user out
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return render(request, 'app/login_page.html') 

        

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
            mapCheck = questionNum.map
            routeID = questionNum.routeID_id
            num = questionNum.questionNum
            info = Questions.objects.filter(node_num=int(num),routeID=routeID)  # Get question from the database using num counter
            request.session['groupcode'] = groupcode         #Add group code into user's session
            request.session['score'] = score            #  Add score into user's session
            request.session['routeID'] = routeID
            if num >1:
                print(num)
                num -=1
                print(num)
                latest_question = Questions.objects.get(node_num=num, routeID=routeID)
                num +=1
            else:
                latest_question = Questions.objects.get(node_num=num , routeID=routeID)
            location = latest_question.location
            longtitude = latest_question.longtitude
            latitude = latest_question.latitude
            place_name = latest_question.answers
            return render(request, 'app/studentview.html',{"groupcode":groupcode, "data":info, "id":id, "score":score,"map_check":mapCheck,"location":location,"longtitude": longtitude,
                                                               "latitude":latitude,"answer":place_name})
        # otherwise show an error message
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
            place_name = latest_question.answers
            map_check = "True"

            num += 1  # Add 1 to the counter so the questions moves on to the next one
            if Questions.objects.filter(node_num=int(num), routeID=routeID).exists():     #Check whether if the user is on the last question
                score += 3
                questionNum.map = map_check
                questionNum.questionNum = num
                questionNum.save()
                print(location)
                info = Questions.objects.filter(node_num=num, routeID=routeID)
                messages.success(request, 'Correct!')  #Generate message saying correct
                return render(request, 'app/studentview.html',{"groupcode":groupcode,"data":info,"id":id,
                                                               "score":score, "map_check":map_check,
                                                               "location":location,"longtitude": longtitude,
                                                               "latitude":latitude,"answer":place_name})

            else:                 #Case when the user is on the last question
                num -=1
                questionNum.questionNum = num
                questionNum.map = map_check
                questionNum.save()
                info = Questions.objects.filter(node_num=num,routeID=routeID)
                messages.success(request, 'You have finished the quiz, well done!')  #Generate message when user finish the quiz
                return render(request, 'app/studentview.html', {"groupcode":groupcode,"data":info,"id":id,
                                                               "score":score, "map_check":map_check,
                                                               "location":location,"longtitude": longtitude,
                                                               "latitude":latitude,"answer":place_name,"Finished":"True"})
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
        mapcheck = questionNum.map
        info = Questions.objects.filter(node_num=int(num), routeID=routeID)  # Get question from the database using num counter
        latest_question = Questions.objects.get(node_num=num-1, routeID=routeID)
        location = latest_question.location
        longtitude = latest_question.longtitude
        latitude = latest_question.latitude
        place_name = latest_question.answers
        return render(request, 'app/studentview.html',
                      {"groupcode": groupcode, "data": info, "id": id, "score": score, "map_check": mapcheck,
                       "location": location, "longtitude": longtitude,
                       "latitude": latitude, "answer": place_name})
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



def set_map_false(request):
    group_num = request.session['groupcode']
    a = Gamecode.objects.get(groupcode = group_num)
    a.map = "False"
    a.save()