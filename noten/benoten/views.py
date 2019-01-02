import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse,request, Http404, HttpResponseRedirect
from django.template import  loader
from django.urls import reverse
from .models import Question,Choice
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'benoten/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last fifty published questions."""
        return Question.objects.order_by('-pub_date')[:15]
        #return HttpResponse("you are voting")


class DetailView(generic.DetailView):
    model = Question
    template_name = 'benoten/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'benoten/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'benoten/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('benoten:results', args=(question.id,)))

    #return HttpResponse("You're voting on question %s." % question_id)