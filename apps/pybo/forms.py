from django import forms
from apps.pybo.models import Question, Answer

"""
    Django 폼에는 상속받는 종류에 따라
        forms.Form -> 폼
        forms.ModelForm -> 모델 폼 이라 부른다.
        모델폼은 모델과 연결된 폼 으로써, 모델 폼 객체를 저장하면,
        연결된 모델의 데이터를 저장할 수 있다.
        모델폼은 반드시 Meta 클래스를 가져야 하며, 
        여기에 모델폼이 사용할 모델과 클래스를 명시해야 한다.
"""


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        # field 는 폼에서 model 에 가져와 연결할 항목들을 나열
        fields = ['subject', 'content']

        # 부트스트랩 (꾸미기) 적용하기 -> 폼의 설정된 태그들에 별도 css 가 적용되게 수정
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
        }

        # 위의 모델에서 가져온 필드의 이름 바꾸기
        labels = {
            'subject': '제목',
            'content': '내용'
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {'content': '답변내용', }
