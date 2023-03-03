from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
    template_name: str = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name: str = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())




class ResultsView(generic.DetailView):
    model = Question
    template_name: str = "polls/results.html"



#def index(req):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]

#    context = {
#            'latest_question_list': latest_question_list,
#        }
#    return render(req, 'polls/index.html', context)

#def detail(req, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    context = {
#            'question': question
#        }
#    return render(req, 'polls/detail.html', context)
    

#def results(req, question_id):
#    question = get_object_or_404(Question, pk=question_id)

#    context = {
#            'question': question,
#        }
#    return render(req, 'polls/results.html',context)

def vote(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=req.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        context = {
                'question': question,
                'error_message': "You have not selected a choice"
            }
        return render(req, 'polls/detail.html', context)
    
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))

