# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader, RequestContext
from models import Question, Choice
from django.core.urlresolvers import reverse

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('poll/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context))
    return render(request, 'poll/index.html', context)


def detail(request, question_id):
    # try:
    #     question = Question.objects.all().get(pk = question_id)
    # except Question.DoesNotExist:
    #     raise Http404('the question does not exist!')
    question = get_object_or_404(Question, pk=question_id)  # 使用django提供的api方法，自动抛出异常
    return render(request, 'poll/detail.html', {'question': question, })


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results.html', {'question': question, })


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selectNum = request.POST['choice_post']
        selectChoice = get_object_or_404(Choice, pk=selectNum)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selectChoice.votes += 1
        selectChoice.save()
        # 在增加Choice的得票数之后，代码返回一个 HttpResponseRedirect而不是常用的HttpResponse
        # 这是约定俗成，为了防止点击返回发生二次post
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))
