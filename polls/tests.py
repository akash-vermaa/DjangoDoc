"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import datetime

from .models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)

    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Polls are not available")
        self.assertQuerysetEqual(res.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        res = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(res.context['latest_question_list'], [question])

    def test_future_question(self):
        create_question(question_text="Future question", days=30)
        res = self.client.get(reverse('polls:index'))
        self.assertContains(res, "Polls are not available")
        self.assertQuerysetEqual(res.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        question = create_question(question_text="past question", days=-30)
        create_question(question_text="future question", days=30)
        res = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(res.context['latest_question_list'], [question])

    def test_two_past_question(self):
        question1 = create_question(question_text="past question 1", days=-10)
        question2 = create_question(question_text="past question 2", days=-20)
        res = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(res.context['latest_question_list'], [question1, question2])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text="Future question", days=5)
        url = reverse('polls:detail', args=[future_question.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)
    
    def test_past_question(self):
        past_question = create_question(question_text="past question", days=-30)
        url = reverse('polls:detail', args=[past_question.id])
        res = self.client.get(url)
        self.assertContains(res, past_question.question_text)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


