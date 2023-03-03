from django.db import models
from django.utils import timezone
from django.contrib import admin

import datetime

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200, help_text='Question')
    pub_date = models.DateTimeField('Date Published')

    @admin.display(boolean=True, ordering='pub_date', description='Published Recently')
    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

    def __repr__(self) -> str:
        return f"Question: {self.question_text}\nPublished On: {self.pub_date}"

    def __str__(self):
        return f"Question: {self.question_text}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def __repr__(self):
        return f"Question:{self.question.question_text}\nChoice: {self.choice_text} (Votes:{self.votes})\n"

