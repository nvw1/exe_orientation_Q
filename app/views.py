# author : Hao, Sam

from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User as auth_user
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
def index(request):
    """
    Display the index page for user
    :param request:
    :return: Returns index page to the user's browser
    """
    """set node num to 1, returns index.html with the request being passed through"""

    # sets the node num to 1 when landing on index page
    return render(request, 'app/index.html')



@login_required(redirect_field_name='', login_url='login_view')  
def game_master_page(request):
    """
    Load game master page, sends all the available routeID's and questions to the game_master_page as objects
    so it can be accessed in the game master page
    :param request:
    :return: Returns view of game master page
    """
    """load game master page"""

    route_list = Routes.objects.all()
    questions = Questions.objects.all()
    games = Gamecode.objects.all()
    return render(request, 'app/game_master_page.html',{"route_list":route_list,"questions":questions,"games":games})
def login_page(request):
    """
    Load login page for user
    :param request:
    :return: Returns view of login page
    """
    """load login page"""
    return render(request, 'app/login_page.html')

def signUp_page(request):
    """load signUp page"""
    return render(request, 'app/signUp_page.html')

def about(request):
    """load about page"""
    return render(request, 'app/about.html')

@login_required(redirect_field_name='')
def manage_account(request):
    """load manage account page"""
    return render(request, 'app/manage_account.html')

def login_view(request):
    """
    It handles login methods,  return game master page if details are correct, also allows signup and change password
    requests
    :param request:
    :return: Return game master page if login details are correct, allows create user and change passwords
    """
    """handle log in methods - button presses, handling user events, handling the database"""

    # if sign up button pressed
    if request.method == 'POST' and 'submit-signUp' in request.POST:
        newUsername = request.POST['username']
        newPassword = request.POST['password']

        # check if username is used
        u = auth_user.objects.get(username=newUsername)
        if u is not None:
            messages.error(request, 'Username already in use')
            return render(request, 'app/signUp_page.html')

        # if u is not None:

        # if the user does not already exist
        # set new user
        print("making new user")
        # if they are a superuser
        if 'superuser' in request.POST:
            newUser = auth_user.objects.create_user(username=newUsername, password=newPassword, is_superuser=True)
        else:
            newUser = auth_user.objects.create_user(username=newUsername, password=newPassword, is_superuser=False)

        # save the user in the database
        newUser.save()
        # log user in
        login(request, newUser)

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
                return render(request, 'app/manage_account.html')
            else:
                messages.error(request, 'passwords did not match')
                return render(request, 'app/manage_account.html')
        else:
            # report errors
            print("log in failure")
            messages.error(request, 'log in failure')
            return render(request, 'app/login_page.html')
    
    if request.method == "POST" and 'submit-deleteAcc' in request.POST:
        user = request.user
        user.is_active = False
        user.save()
        messages.success(request, 'Account successfully deactivated')
        return render(request, 'app/login_page.html')


    print("did not get username or password")
    messages.error(request, 'did not get username or password')
    return render(request, 'app/login_page.html')

def logout_view(request):
    """
    Log out the current signed in user
    :param request:
    :return: Return login page when user wants to sign out
    """
    """log out handling"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return render(request, 'app/login_page.html')



def redirect(request):
    """
    Handling what happens when the groupcode is submitted by user and handles input from user's when they are answering
    questions.
    :param request:
    :return: The methods returns the student view page which is the actual game to the user if they entered a correct
    groupcode, it will also return messages when user's are answering questions in the quiz telling them if the answers
    are correct or not
    """
    """handling what happens when the groupcode is entered and submitted aswell as the question logic"""
    global score
    global num
    map_check = False
    # Below is to check if whether the button is for groupcode or answer to question
    # process the group code passed from the landing page
    if request.method == 'POST' and 'submit-groupcode' in request.POST:
        # Get inputted groupcode from the user
        groupcode = str(request.POST.get('groupCode'))
        # if the group code exists, load the treasure hunt page with the correct questions
        if Gamecode.objects.filter(groupcode=groupcode).exists():
            #Below is for question loading and getting question informations
            questionNum = Gamecode.objects.get(groupcode=groupcode)
            mapCheck = questionNum.map
            routeID = questionNum.routeID_id
            num = questionNum.questionNum
            score = questionNum.score
            # Get question by using the question number the group is currently on
            info = Questions.objects.filter(node_num=int(num),routeID=routeID)
            # Add group code into user's session
            request.session['groupcode'] = groupcode
            # Add score into user's session
            request.session['score'] = score
            # Add routeID into user's session
            request.session['routeID'] = routeID
            #To show the correct map for the user to go to when the join the game after a question is answered but the
            # map check is not yet done
            if num >1:
                print(num)
                #set map value to the previous question
                num -=1
                print(num)
                latest_question = Questions.objects.get(node_num=num, routeID=routeID)
                #Return number to the correct question number
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
        # Get routeID from user's session
        routeID = request.session['routeID']
        # Get groupcode from user's session
        groupcode = request.session['groupcode']
        # Get text from the input answer box
        data = str(request.POST.get('answer'))
        # Retrieve the current question the group is on from the database
        questionNum = Gamecode.objects.get(groupcode=groupcode)

        # if answer is correct for the current node, move onto the next question if it exists,
        # otherwise show they have finished the quiz
        if Questions.objects.filter(answers__icontains=data.strip(), node_num=int(num), routeID=routeID).exists():

            latest_question = Questions.objects.get(node_num=num, routeID=routeID)
            location = latest_question.location
            longtitude = latest_question.longtitude
            latitude = latest_question.latitude
            place_name = latest_question.answers
            map_check = "True"
            # Add 1 to the counter so the questions moves on to the next one
            num += 1
            # Check whether if the user is on the last question
            if Questions.objects.filter(node_num=int(num), routeID=routeID).exists():
                score += 3
                questionNum.map = map_check
                questionNum.questionNum = num
                questionNum.score = score
                questionNum.save()
                print(location)
                info = Questions.objects.filter(node_num=num, routeID=routeID)
                messages.success(request, 'Correct!')  #Generate message saying correct
                return render(request, 'app/studentview.html',{"groupcode":groupcode,"data":info,"id":id,
                                                               "score":score, "map_check":map_check,
                                                               "location":location,"longtitude": longtitude,
                                                               "latitude":latitude,"answer":place_name})
            # Case when the user is on the last question
            else:
                # To make sure user stays on the last question
                num -=1
                questionNum.questionNum = num
                questionNum.map = map_check
                questionNum.save()
                info = Questions.objects.filter(node_num=num,routeID=routeID)
                # Generate message when user finish the quiz
                messages.success(request, 'You have finished the quiz, well done!')
                # Return the information back to user's view
                return render(request, 'app/studentview.html', {"groupcode":groupcode,"data":info,"id":id,
                                                               "score":score, "map_check":map_check,
                                                               "location":location,"longtitude": longtitude,
                                                               "latitude":latitude,"answer":place_name,"Finished":"True"})
        # Case when user gets the answer wrong
        else:
                info = Questions.objects.filter(node_num=num, routeID=routeID)
                # Return incorrect message
                messages.error(request, 'That is the wrong answer, please try again')
                # Return the information back to user's view
                return render(request, 'app/studentview.html', {"groupcode": groupcode, "data": info, "id": id,"score":score})


    # Case when user refreshes the page during the game
    if 'groupcode' in request.session:
        # Retrieve information about the questions
        groupcode = request.session['groupcode']
        routeID = request.session['routeID']
        questionNum = Gamecode.objects.get(groupcode=groupcode)
        num = questionNum.questionNum
        mapcheck = questionNum.map
        # Get question from the database using num counter
        info = Questions.objects.filter(node_num=int(num), routeID=routeID)
        if num > 1:
            print(num)
            # set map value to the previous question
            num -= 1
            print(num)
            latest_question = Questions.objects.get(node_num=num, routeID=routeID)
            # Return number to the correct question number
            num += 1
        else:
            latest_question = Questions.objects.get(node_num=num, routeID=routeID)
        location = latest_question.location
        longtitude = latest_question.longtitude
        latitude = latest_question.latitude
        place_name = latest_question.answers
        # Return the information back to user's view
        return render(request, 'app/studentview.html',
                      {"groupcode": groupcode, "data": info, "id": id, "score": score, "map_check": mapcheck,
                       "location": location, "longtitude": longtitude,
                       "latitude": latitude, "answer": place_name})
    else:
        # Redirect user back to start page
        return render(request, 'app/index.html')


def hint(request):
    """
    Retrieve hints of the question user
    :param request:
    :return: Returns the hint information retrieve from the database to the html page
    """
    global score
    hint = Questions.objects.values_list('hints', flat=True).filter(node_num=num)
    score1 = request.POST.get('score')        #  Get score from ajax request
    request.session['score'] = score1      # update score variable
    score = int(score1)
    # Return the information back to html page's ajax call
    return HttpResponse(hint)


def update_request(request):
    """
    Check if user's current question is the same one in the database so that if one user in the group answers the
    question the question gets updated
    :param request:
    :return: Returns a reponse to the ajax call
    """
    """update the request if there is a difference between the question the user is on and the question on the request"""
    question_num = request.POST.get('current_question')
    group_num = request.session['groupcode']
    latest_question = Gamecode.objects.get(groupcode=group_num)
    latest_num = latest_question.questionNum
    # Check if the question user is on is same as the group's latest question,
    if int(question_num) != int(latest_num):
        return HttpResponse("Not the same")
    else:
        return HttpResponse("Same Question")

def reset_question(request):
    """

    :param request:
    :return:
    """
    """testing only - reset the questions in the current game"""
    global num
    t = Gamecode.objects.get(groupcode='0001')
    t.questionNum = '1'
    t.save()
    num = 1


##loading pages
def health(request):
    """
    return the status of the session", used by the server to handle errors
    :param request:
    :return: return the status of the session"
    """
    state = {"status": "UP"}
    return JsonResponse(state)


def handler404(request):
    """
    rendering 404 page, used by the server to handle errors
    :param request:
    :return: rendering 404 page
    """
    return render(request, '404.html', status=404)


def handler500(request):
    """
    rendering the 500 page, used by the server to handle errors
    :param request:
    :return: rendering the 500 page
    """

    return render(request, '500.html', status=500)


def studentview(request):
    """
    Rendering the student view page
    :param request:
    :return: Return the student view page
    """
    return render(request,'app/studentview.html')


def faq(request):
    """
    Render the FAQ page
    :param request:
    :return: Return the FAQ page
    """
    return render(request,'app/FAQ.html')


def contact(request):
    """
    Render the contact page
    :param request:
    :return: Return the contact page
    """
    return render(request,'app/contact.html')

def locations(request):
    """render the locations page"""
    return render(request, 'app/locations.html')

#creating route
def create_route(request):
    """
    handling requests when gamemaster is trying to create a new routeID
    :param request:
    :return: Return a reponse to ajax call to tell it whether create routeID has been successful or not
    """
    """logic  for creating a custom route"""
    # Get routeID from ajax request
    routeId = request.POST.get('data2')
    # Get routeName from ajax request
    routeName = request.POST.get('routeName')
    number = 0
    #getting rid of extra string of the variable from the ajax request
    for i in range(len(routeId)):
        if routeId[i] == "=":
            number = i
    routeId= routeId[number+1::]

    # Check if the routeID user is trying to create already exist in the database
    if Routes.objects.filter(routeID=int(routeId)).exists():
        return HttpResponse("Exist")
    else:
        # If route doesn't exist then create the route
        # Create a new instance in the database with the given routeID and routeName
        c = Routes.objects.create(routeID = routeId, RouteName = routeName, gameMaster_GMID_id=1, Node = "1", NodeID= 1)
        # Save the instance
        c.save()
        c.refresh_from_db()
        print("Hello")
        return HttpResponse("Does not exist")


def add_question(request):
    """
    Add questions details retrieved from the ajax call and save it to the database
    :param request:
    :return: Return a reponse to ajax call whether the question has been added successfully or not
    """
    #adding question - getting data through post request
    question = request.POST.get('question')
    answer = request.POST.get('answer')
    hint = request.POST.get('hint')
    latitude = request.POST.get('latitude')
    longtitude = request.POST.get('longtitude')
    node_num = request.POST.get('node_num')
    routeID = request.POST.get('routeID')
    routeID = striptext(routeID)
    #
    print(question,answer,hint,latitude,longtitude,node_num,routeID)
    #setting up questions object
    b = Questions()
    b.questions = question
    b.answers = answer
    b.hints = hint
    b.latitude = float(latitude)
    b.longtitude = float(longtitude)
    b.node_num = int(node_num)
    b.routeID_id = int(routeID)
    # Save instance into database
    b.save()
    #checking if the questions were added successfully or not
    if Questions.objects.filter(questions=question).exists():
        return HttpResponse("Added successfully")
    else:
        return HttpResponse("Not added")


def striptext(variable):
    """
    stripping text before an equals sign - getting all data after the equals
    :param variable:
    :return: Return data after equals sign
    """
    """stripping text before an equals sign - getting all data after the equals"""
    number = 0
    for i in range(len(variable)):
        if variable[i] == "=":
            number = i
            break
    return variable[number+1::]


def create_game(request):
    """
    Create the game - getting the groupcode and routeID and save it to the database
    :param request:
    :return: Return a reponse to the ajax call whether the the instance has been successfully saved into the database
    or not
    """
    groupcode1 = request.POST.get("groupcode")
    routeID = request.POST.get("routeID")
    # Check if the groupcode already exist
    if Gamecode.objects.filter(groupcode=groupcode1).exists():
        return HttpResponse("Exist")
    else:
        # Add groupcode to database
        a = Gamecode()
        a.groupcode = groupcode1
        a.routeID_id= routeID
        a.score = 0
        # Save instance
        a.save()
        return HttpResponse("Added")



def set_map_false(request):
    """
    Set map column to false in the database for the group after someone has verified their location
    :param request:
    :return:
    """
    group_num = request.session['groupcode']
    a = Gamecode.objects.get(groupcode = group_num)
    a.map = "False"
    a.save()



def delete_question(request):
     """
     Delete the selected question from the ajax call from the database
     :param request:
     :return:
     """
     routeID = request.POST.get('routeID')
     node_num = request.POST.get('node_num')
     # Check if the question actually exist in the database before deleting the entry
     if Questions.objects.filter(routeID=routeID, node_num=node_num).exists():
         a = Questions.objects.get(routeID=routeID, node_num=node_num)
         a.delete()
         return HttpResponse("Deleted successfully")
     # Return error message if the record user is trying to delete does not exist
     else:
         return HttpResponse("Not exist")




def edit(request):
    """
    Allows user's to edit field values of an entry in the questions database
    :param request:
    :return: A reponse message to ajax on whether the field has been edited successfully or not
    """
    # Get the information that user want to store from ajax call
    question = request.POST.get('question')
    answer = request.POST.get('answer')
    hint = request.POST.get('hint')
    latitude = request.POST.get('latitude')
    longtitude = request.POST.get('longtitude')
    node_num = request.POST.get('node_num')
    routeID = request.POST.get('routeID')
    # Retrieve the question and change the details
    b = Questions.objects.get(node_num=node_num, routeID=routeID)
    b.questions = question
    b.answers = answer
    b.hints = hint
    print(latitude,longtitude,"hello")
    b.latitude = float(latitude)
    b.longtitude = float(longtitude)
    b.node_num = int(node_num)
    b.routeID_id = int(routeID)
    # Save the instance to the database
    b.save()
    if Questions.objects.filter(questions=question).exists():
        return HttpResponse("Added successfully")
    else:
        return HttpResponse("Not added")




def add_question_existing(request):
    """
    Allow user to add question to an existing route to the database
    :param request:
    :return: Return a response to ajax call on whether the question has been added successfully
    """
    # Get the values that user want to add into the database
    question = request.POST.get('question')
    answer = request.POST.get('answer')
    hint = request.POST.get('hint')
    node_num = 1
    latitude = request.POST.get('latitude')
    longtitude = request.POST.get('longtitude')
    routeID = request.POST.get('routeID')
    # Make the node number of the new question to be added highest out of all the node number with the same routeID
    while Questions.objects.filter(node_num=node_num, routeID=routeID).exists():
        node_num += 1
        print(node_num)
    b = Questions()
    b.questions = question
    b.answers = answer
    b.hints = hint
    b.latitude = float(latitude)
    b.longtitude = float(longtitude)
    b.node_num = int(node_num)
    b.routeID_id = int(routeID)
    b.save()
    if Questions.objects.filter(questions=question).exists():
        return HttpResponse("Added successfully")
    else:
        return HttpResponse("Not added")


def delete_route(request):
    """
    Deleted a route from the database
    :param request:
    :return: Returns a reponse to ajax call on whether the route has been successfully deleted or not
    """
    routeID = request.POST.get('routeID')
    print(routeID)
    # Check if route exist
    if Routes.objects.filter(routeID=int(routeID)).exists():
        # Delete the routeID entry from the database
        a = Routes.objects.get(routeID=int(routeID))
        a.delete()
    # Check if there are questions with the deleted routeID
    if Questions.objects.filter(routeID=int(routeID)).exists:
        # Delete all the question entry which has the same routeID as the one deleted
        Questions.objects.filter(routeID=int(routeID)).delete()
        return HttpResponse("Deleted successfully")
    else:
        return HttpResponse("Not exist")
