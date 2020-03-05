# -*- coding: utf-8 -*-
#author :  Hao
from django.db import models

# Create your models here.

#Used for the game
class Gamecode(models.Model):
    groupcode = models.CharField(max_length=250)

    def __str__(self):     #convert objects in to strings
        return self.groupcode

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


class Questions(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    questions = models.CharField(max_length=100)
    answers = models.CharField(max_length=100)
    node_num = models.IntegerField()
    hints = models.CharField(max_length=100)

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

class Groups(models.Model):
    GroupID = models.AutoField(primary_key=True)
    GroupName = models.CharField(max_length=45)
    Players_playerID = models.ForeignKey(Players, on_delete=models.DO_NOTHING)


Questions.objects.all()
question = "Where is the library located?"

if Questions.objects.filter(questions=question.strip()).exists():
    pass
    print("exist")
else:
    a = Questions(questions=question, answers="The forum",node_num=1,hints="the name also refers to discussion board on the Internet")
    a.save()

question = "Which is the tallest building on campus?"
if Questions.objects.filter(questions=question.strip()).exists():
    print("exist")
    pass
else:
    b= Questions(questions="Which is the tallest building on campus?", answers="Physics building",node_num=2, hints = "What subject did albert einstein study in?")
    b.save()
