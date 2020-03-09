# author : Hao, Sam

from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.http import Http404
from app.models import Gamecode
from app.models import Questions

# current node number, global variable
num = 1
score = 0

def index(request):
    # sets the node num to 1 when landing on index page
    global num
    num = 1
    return render(request, 'app/index.html')


@login_required(redirect_field_name='')
def game_master(request):
    return render(request,'app/game_master_page.html')

def login_page(request):
    return render(request, 'app/login_page.html')

def login_view(request):
    if request.method == 'POST' and 'submit-signUp' in request.POST:
        newUsername = request.POST['username']
        newPassword = request.POST['password']

        # if the user does not already exist
        # if not User.objects.filter(username=newUsername).exist():
        # set new user
        print("making new user")
        newUser = User.objects.create_user(username=newUsername, password=newPassword)
        newUser.save()

        login(request, newUser)

        messages.success(request, 'Login Success')
        return render(request, 'app/game_master_page.html')

        # else:
        #     print("User already exists")
        #     messages.error(request, 'Username already exists')
        #     return render(request, 'app/game_master_page.html')

    if request.method == 'POST' and 'submit-logIn' in request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print("logged in")
            messages.success(request, 'log in success')
            return render(request, 'app/game_master_page.html')
        else:
            print("log in failure")
            messages.error(request, 'log in failure')
            return render(request, 'app/login_page.html')

    print("did not get username or password")
    messages.error(request, 'did not get username or password')
    return render(request, 'app/login_page.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'did not get username or password')
    return render(request, 'app/index.html') 



@login_required
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
            num = questionNum.questionNum
            print(Gamecode.objects.all())
            info = Questions.objects.filter(node_num=int(num))  # Get question from the database using num counter
            request.session['groupcode'] = groupcode         #Add group code into user's session
            request.session['score'] = score            #  Add score into user's session
            return render(request, 'app/studentview.html',{"groupcode":groupcode, "data":info, "id":id, "score":score})


        # otherwise show an error message
        else:
            print("Wrong")
            messages.error(request, 'The game code does not exist')
            return render(request, 'app/index.html')

    # if an answer to question is submitted, check if it is correct
    if request.method == 'POST' and 'submit-question' in request.POST:


        groupcode = request.session['groupcode']            #Get groupcode from user's sessio
        data = str(request.POST.get('answer'))              #Get text from the input answer box
        questionNum = Gamecode.objects.get(groupcode=groupcode)

        # if answer is correct for the current node, move onto the next question if it exists, 
        # otherwise show they have finished the quiz
        if Questions.objects.filter(answers__icontains=data.strip(), node_num=int(num)).exists(): #Check if user get's the answer correct

            latest_question = Questions.objects.get(node_num=num)
            location = latest_question.location
            longtitude = latest_question.longtitude
            latitude = latest_question.latitude
            map_check = True
            num += 1  # Add 1 to the counter so the questions moves on to the next one
            if Questions.objects.filter(node_num=int(num)).exists():     #Check whether if the user is on the last question
                score += 3
                questionNum.questionNum = num
                questionNum.save()
                print(location)
                info = Questions.objects.filter(node_num=num)
                messages.success(request, 'Correct!')  #Generate message saying correct
                return render(request, 'app/studentview.html',{"groupcode":groupcode,"data":info,"id":id,
                                                               "score":score, "map_check":map_check,
                                                               "location":location,"longtitude": longtitude,
                                                               "latitude":latitude})

            else:                 #Case when the user is on the last question
                questionNum.questionNum = num
                questionNum.save()
                info = Questions.objects.filter(node_num=num)
                messages.success(request, 'You have finished the quiz, well done!')  #Generate message when user finish the quiz
                return render(request, 'app/studentview.html', {"groupcode": groupcode, "data": info, "id": id,"score":score})
        else:         # Case when user gets the answer wrong

            info = Questions.objects.filter(node_num=num)
            messages.error(request, 'That is the wrong answer, please try again')
            # Return incorrect message
            return render(request, 'app/studentview.html', {"groupcode": groupcode, "data": info, "id": id})
    if 'groupcode' in request.session:
        groupcode = request.session['groupcode']
        questionNum = Gamecode.objects.get(groupcode=groupcode)
        num = questionNum.questionNum
        info = Questions.objects.filter(node_num=int(num))  # Get question from the database using num counter
        return render(request, 'app/studentview.html', {"groupcode": groupcode, "data": info, "id": id,"score":score})
    else:
        num = 1
        return render(request, 'app/index.html')
    print(request.method)


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

