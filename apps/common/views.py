from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from apps.common.forms import UserForm


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # form.cleaned_data.get -> 회원가입에서 폼에 입력된 값을 얻기 위하여 사용하는 함수.
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # authenticate()는 인증정보를 통하여 사용자 인증 후, user 객체를 반환하는 함수.
            user = authenticate(username=username, password=raw_password)
            # login()은 해당 객체정보를 통하여 로그인을 수행하는 함수.
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
