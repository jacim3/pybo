from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import QuestionForm, AnswerForm

from apps.pybo.models import Question, Answer


# 메인 게시판 화면
def index(request):
    # 작성일시를 기준으로 정렬. -가 붙으므로 내림차순 -> 최신 게시글이 맨 위에서 보이도록
    question_list = Question.objects.order_by('-create_date')

    # 페이징 -> 리스트를 get 요청 방식과 일정 기준에 따라 분할하여 가독성을 높이는 기법 ex. localhost:8000/pybo/?page=4
    # 1. 우선 페이징 변수를 선언
    page = request.GET.get('page', '1')  # 페이징 방식은 get 방식으로 처리하며 이 때, 해당 값을 받을 page 변수는 page, 기본값은 1
    """
        page_obj 의 속성
        
        항목	설명
        paginator.count	        전체 게시물 개수
        paginator.per_page	    페이지당 보여줄 게시물 개수
        paginator.page_range	페이지 범위
        number	                현재 페이지 번호
        previous_page_number	이전 페이지 번호
        next_page_number	    다음 페이지 번호
        has_previous	        이전 페이지 유무
        has_next	            다음 페이지 유무
        start_index	            현재 페이지 시작 인덱스(1부터 시작)
        end_index	            현재 페이지의 끝 인덱스(1부터 시작)
    """
    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 한 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    # context = {'question_list': question_list}  # 페이징 기법을 이용함으로써, 단순히 컨텍스트를 보내는 방법은 불필요해짐
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)


# 게시글 클릭했을 때 상세정보 보이기 -> question_list.html 의 게시글에 걸려있는 href 속성을 통하여 요청 및 id 를 받으므로,
# 이에대한 요청을 처리하기 위하여 사용된다.
def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    # ↑ 객체를 받아오지 못할 경우, 오류 대신 404를 반환하도록.
    question = get_object_or_404(Question, id=question_id)
    context = {'question': question}

    return render(request, 'pybo/question_detail.html', context)


# login_required 어노테이션을 붙임으로써, 로그인이 되지 않았을 경우의 우회 url 경로를 지정할 수 있다. 또한 url 에 next 속성이 추가로 붙음으로써,
# 요청 처리만 관리하는 메서드 이므로, 따로 템플릿이 필요 없다. 아래의 render 는 오류화면을 보여주기 위하여 사용함(redirect 는 새로고침을 일으킨다.)
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    # content = request 에서 전달받은 내용 중 textarea 의 내용만 추출하기 위하여 사용.
    # 해당 객체를 참조하는 answer 객체를 생성.
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            # 모델에 추가된 author 필드에 대한 정보를 가져옴
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


# 질문 등록을 사용하기 위한 메서드
@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        # get 방식의 경우 추가적인 매개변수가 필요 없으나,
        # post 방식의 경우 전달받은 데이터를 form 에 별도로 전달해 주어야 한다.
        form = QuestionForm(request.POST)
        # request 로 받은 form 이 유요한지 검사함
        if form.is_valid():
            # form 으로 Question 모델 데이터를 저장하기 위한 코드 commit=False 는 임시저장을 의미
            # 즉, 실제 데이터는 저장되지 않은 상태로서, 임시저장을 사용하는 이유는, 폼으로 질문 데이터를 저장할 경우,
            # Question 모델의 create_date 값이 설정되지 않아 오류가 발생하기 때문
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    # 맨 처음 호출되었을 때, post 요청이 일어나지 않으므로, 빈 폼을 로드하기 위한 else 초건이 먼저 수행된다.
    else:
        form = QuestionForm()
    # form 은 템플릿에서 form element 를 생성할 때 사용하는 변수
    # 빈 값이 들어가는 등 페이지 로딩이 한번 끝났는데도 불구,

    return render(request, 'pybo/question_form.html', {'form': form})


def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')

        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        # instance 에 question 을 저장 시 기존 정보가 채워진 상태를 유지시켜 준다.
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()

            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}

    return render(request, 'pybo/question_form.html', context)


def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error("글 삭제권한이 없습니다")

        return redirect('pybo:detail', question_id=question_id)
    question.delete()
    return redirect('pybo:index')


def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)
