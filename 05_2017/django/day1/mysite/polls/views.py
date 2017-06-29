from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Choice, Question
from django.utils import timezone
from django.db.models import Sum
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


def index(request):
    question_list = Question.objects.filter(pub_date__lt=timezone.now()).order_by('-pub_date')
    context = {'question_list': question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    err_message = ''
    vote_count = question.choice_set.aggregate(Sum('votes'))['votes__sum']
    if vote_count is None:
        vote_count = 0

    return render(request, 'polls/detail.html', {'question' : question,
                                                 'error_message' : err_message,
                                                 'vote_count' : vote_count})


def add_question(request):
    question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'question_list': question_list}
    question_text = request.POST['question_text']
    for q in Question.objects.all():
        if q.question_text == question_text:
            return render(request, 'polls/index.html', context)
    quest = Question(question_text=question_text, pub_date=timezone.now())
    quest.save()
    return HttpResponseRedirect(reverse('index'))


def add_choice(request, question_id):
    choice_text = request.POST['choice_text']
    question = get_object_or_404(Question, pk=question_id)
    for choice in question.choice_set.all():
        if choice_text == choice.choice_text:
            break
    else:
        choice = Choice(question=question, choice_text=choice_text)
        choice.save()
    return HttpResponseRedirect(reverse('detail', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question' : question})


def send_mail(subject, message, sender, recipients):
    pass


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('results', args=(question.id,)))


def register(request, *args, **kwargs):
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    if email and password:
        user, created = User.objects.get_or_create(username=email,
                                                   email=email)
        if created:
            user.set_password(password)
            user.save()

        user = authenticate(username=email, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))
# return error or redirect to login page again
