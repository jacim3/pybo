from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import QuestionForm, AnswerForm

from apps.pybo.models import Question


# 메인 게시판 화면
def index(request):
    # 작성일시를 기준으로 정렬. -가 붙으므로 내림차순
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}

    return render(request, 'pybo/question_list.html', context)


# 게시글 클릭했을 때
def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    # 객체를 받아오지 못할 경우, 오류 대신 404를 반환하도록.
    question = get_object_or_404(Question, id=question_id)
    context = {'question': question}

    return render(request, 'pybo/question_detail.html', context)


# https://wikidocs.net/70855
# 요청 처리만 관리하는 메서드 이므로, 따로 템플릿이 필요 없다. 아래의 render 는 오류화면을 보여주기 위하여 사용함
def answer_create(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    # content = request 에서 전달받은 내용 중 textarea 의 내용만 추출하기 위하여 사용.
    # 해당 객체를 참조하는 answer 객체를 생성.
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


def question_create(request):
    if request.method == 'POST':
        # get 방식의 경우 매개변수가 필요 없으나,
        # post 방식의 경우 전달받은 데이터를 form 에 별도로 전달해 주어야 한다.
        form = QuestionForm(request.POST)
        # request 로 받은 form 이 유요한지 검사함
        if form.is_valid():
            # form 으로 Question 모델 데이터를 저장하기 위한 코드 commit=False 는 임시저장을 의미
            # 즉, 실제 데이터는 저장되지 않은 상태로서, 임시저장을 사용하는 이유는, 폼으로 질문 데이터를 저장할 경우,
            # Question 모델의 create_date 값이 설정되지 않아 오류가 발생하기 때문
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    # form 은 템플릿에서 폼 element 를 생성할 때 사용하는 변수
    return render(request, 'pybo/question_form.html', {'form': form})
