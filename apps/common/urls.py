from django.urls import path

from apps.common import views
from django.contrib.auth import views as auth_views

app_name = 'common'

urlpatterns = [

    # 로그인 기능은 Django 의 기본 제공 기능인 auth_views 를 사용 사용. 대신, settings/py 에 LOGIN_REDIRECT_URL 속성을 제공해 준다.
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='common/login.html'), name='logout'),
    path('signup/', views.signup, name='signup'),
]
