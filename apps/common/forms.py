from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


# 기본적으로 사용자 이름, 비번1, 비번2의 항목을 기본으로 가진, 폼 클래스를 상속하여 만든 폼
class UserForm(UserCreationForm):
    # 이메일 항목을 별도로 추가 이를 명시함으로써, form 에서 해당 객체(emil)에 접근할 수 있다.
    email = forms.EmailField(label="이메일")
    # 고유 값을 주고 싶으면....?
    nickname = forms.CharField(max_length=20, required=True)

    # 참조하여 사용할 모델을 명시
    class Meta:
        model = User
        # 굳이 비밀번호는 없는 이유가...???? 보안상의 이유인가...
        fields = ("username", "email", 'nickname')
