from django.shortcuts import render
from .models import Question
from django.utils import timezone

# Create your views here.
def IndexView(req):
	latest_question_list = Question.all()
	print(latest_question_list)
	context = {
			'latest_question_list': latest_question_list
		}

	return render(req, 'mpolls/index.html', context)

def DetailView(req, question_id):
	question = Question.get({'question_id'})
