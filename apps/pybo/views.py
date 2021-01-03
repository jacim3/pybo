from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from apps.pybo.models import Question


def index(request):
    # 작성일시를 기준으로 정렬. -가 붙으므로 내림차순
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    # 객체를 받아오지 못할 경우, 오류 대신 404를 반환하도록.
    question = get_object_or_404(Question, id=question_id)
    context = {'question': question}

    return render(request, 'pybo/question_detail.html', context)


# 요청 처리만 관리하는 메서드 이므로, 따로 템플릿이 필요 없다.
def answer_create(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    # content = request 에서 전달받은 내용 중 textarea 의 내용만 추출하기 위하여 사용.
    # 해당 객체를 참조하는 answer 객체를 생성.
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('pybo:detail', question_id=question_id)
