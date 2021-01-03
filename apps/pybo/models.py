from django.db import models


class Question(models.Model):
    # 글자수를 제한하고 싶은 경우
    subject = models.CharField(max_length=200)
    # 글자수를 제한하지 않는 값을 가질 경우
    content = models.TextField()
    # 날짜, 시간 관련 속성들 저장
    create_date = models.DateTimeField()

    # 해당 모델이 출력되었을 때, 이에대한 객체의 표현 형식을 정의
    def __str__(self):
        return self.subject + " " + self.content


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

    """
        데이터 만들고 조회하기
        
        1. python manage.py shell 입력
        
        2. from apps.pybo.models import Question, Answer을 통하여 등록
        
        3. 입력 
            - from django.utils import timezone -- 현재 시간 가져오기 위하여.
            - q = Question(subject='pybo가 무엇인가요?', content='pybo에 대해서 알고 싶습니다.', create_date=timezone.now())
            - q.save()
            
        4. 출력
         q.id --> 1 
         모델 모두 조회 = Question.objects.all()
            특정 조건만 조회하고 싶은 경우 -> Question.objects.filter(조건식(ex. id=1))
            단, 여러개가 있을 경우, 조건에 맞는건 모두 조회하므로, 하나만 조회하고 싶을 경우, get(조건식)을 사용할 것!!!
            
        5. 수정
           - 우선 변경하고자 하는 데이터를 검색하여 변수에 할당한다. ex. q = Question.object.get(id=1) -- 반드시 'get()'으로 조회한 값으로 할당해야 한다.
           - 해당 변수의 속성값을 수정 ex. q.subject = 'asdf'
           - 저장 ex. q.save()
           
       6. 삭제
           - 수정과 같이, get()을 사용해 조회한 값을 특정 변수에 할당.
           - delete()함수를 사용하여 삭제.
           - 중간의 삭제되어도 기본키가 옮겨지는 등의 변화가 생기지 않는다.
           
       7. 외래키 넣기
           - 외래키의 대상이 되는 기본키 객체를 별도의 변수에 할당 ex. q = Question.objects.get(id=2)
           - 해당 객체를 외래키로 받을 모델객체 생성 후 변수에 할당 ex. a = Answer(question=q, content='네 자동으로 생성됩니다.', create_date=timezone.now())
           - 저장 ex. a.save() 
           - Django 에서는 ORM 을 통하여, 단순 외래키로 연결이 된 것이 아닌, 객체끼리의 연결관계를 갖는다. 이렇게 의존하는 객체 또한 id를 통하여 기본키를 갖으며, 이는 별도의 키
           이므로, 객체간의 연결과는 관계가 없다. 대신, 연결된 객체를 통하여 해당 객체를 곧바로 호출하여 출력이 가능하다. 
           
       8. answer_set 함수
           - 게시물 : 답변과 같이 1:N의 관계를 갖는 대상에 대하여 이러한 관계를 표현하기 위하여 사용한다.
           - ORM 관계에선 객체를 외래키로 받으므로, 이러한 기준으로 연결된 대상 객체들에 접근하기 위하여 사용한다. ex. q.answer_set.all()     
    
    """
