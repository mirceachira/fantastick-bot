import datetime
from django.utils import timezone
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


class AppUser(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Notification(models.Model):
    appuser = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    notification_text = models.CharField(max_length=500)
    when_date = models.DateTimeField('Date published')
    category = models.CharField(max_length=200)

    

    def __str__(self):
        return self.notification_text

    @staticmethod
    def get_latest():
        a = Notification.objects.order_by('-when_date')[0]
        return a
    @staticmethod
    def get_geometry():
        g = Notification.objects.


    #user = models.ForeignKey(AppUser,                     # App user Foreign key
    #when = # date
    #category = # charfield , exam, class, beer
    #subject = ' # charfiedl    algebra, geometrye       iesier infinit
    #Cand avem examen la geometrie?