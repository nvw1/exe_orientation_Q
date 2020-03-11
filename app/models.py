# -*- coding: utf-8 -*-
#author :  Hao
from django.db import models

# Create your models here.

#Used for the game


#Below table is for testing
# class Musician(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     instrument = models.CharField(max_length=100)

# class Album(models.Model):
#     artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     release_date = models.DateField()
#     num_stars = models.IntegerField()



class User(models.Model):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45)


class Developers(models.Model):
    devID = models.AutoField(primary_key=True)
    user_userID = models.ForeignKey(User, on_delete=models.CASCADE)


class gameMaster(models.Model):
    GMID = models.AutoField(primary_key=True)
    user_userID = models.ForeignKey(User, on_delete=models.CASCADE)


class Routes(models.Model):
    routeID = models.IntegerField(blank=False, null=False, primary_key=True)
    Node = models.CharField(max_length = 45)
    NodeID = models.IntegerField()
    RouteName = models.CharField(max_length = 45)
    gameMaster_GMID = models.ForeignKey(gameMaster, on_delete=models.DO_NOTHING)


class Hints(models.Model):
    HintText = models.CharField(max_length = 100, primary_key = True)
    HintNo = models.IntegerField()
    Routes_routeID = models.ForeignKey(Routes, on_delete=models.DO_NOTHING)
    Routes_NodeID = models.IntegerField()

class Players(models.Model):
    playerID = models.AutoField(primary_key=True)
    user_userID = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Questions(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    questions = models.CharField(max_length=100)
    answers = models.CharField(max_length=100)
    node_num = models.IntegerField()
    hints = models.CharField(max_length=100,default="")
    location = models.CharField(max_length=1000,default="")
    longtitude = models.FloatField(default=-1.1)
    latitude = models.FloatField(default=-1.1)
    routeID = models.ForeignKey(Routes, on_delete=models.CASCADE,default=1)



class Groups(models.Model):
    GroupID = models.AutoField(primary_key=True)
    GroupName = models.CharField(max_length=45)
    Players_playerID = models.ForeignKey(Players, on_delete=models.DO_NOTHING)


class Gamecode(models.Model):
    groupcode = models.CharField(max_length=250)
    questionNum = models.IntegerField(default=1)
    routeID = models.ForeignKey(Routes, on_delete=models.CASCADE,default=1)
    map = models.CharField(max_length=50,default = "False")
    def __str__(self):     #convert objects in to strings
        return self.groupcode


Questions.objects.all()
question = "Where is the library located?"


if Questions.objects.filter(questions=question.strip()).exists():
    pass
else:
    a = Questions(questions=question, answers="The forum",node_num=1,hints="the name also refers to discussion board on the Internet")
    a.save()

question = "Which is the tallest building on campus?"
if Questions.objects.filter(questions=question.strip()).exists():
    pass
else:
    b= Questions(questions="Which is the tallest building on campus?", answers="Physics building",node_num=2, hints = "What subject did albert einstein study in?")
    b.save()

question = "A place where new ideas are produced"

if Questions.objects.filter(questions=question.strip()).exists():
    pass
else:
    a = Questions(questions=question, answers="Innovation centre",node_num=3,hints="It is past the Harrison Building",
                  location= "https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d10100.076253535459!2d-3.5306391!3d50.7381353!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x9a5f61816c99672c!2sThe%20Innovation%20Centre!5e0!3m2!1sen!2suk!4v1583711670328!5m2!1sen!2suk",
                  latitude= 50.738162, longtitude=-3.530587)


    a.save()
