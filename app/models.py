# -*- coding: utf-8 -*-
#author :  Hao
from django.db import models

# Create your models here.

#Used for the game
class Gamecode(models.Model):
    groupcode = models.CharField(max_length=250)
    questionNum = models.IntegerField(default=1)
    def __str__(self):     #convert objects in to strings
        return self.groupcode





class Questions(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    questions = models.CharField(max_length=100)
    answers = models.CharField(max_length=100)
    node_num = models.IntegerField()
    hints = models.CharField(max_length=100,default="")





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
