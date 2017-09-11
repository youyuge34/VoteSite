# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader, RequestContext
from models import Question


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
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
