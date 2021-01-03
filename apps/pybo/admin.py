from django.contrib import admin

from apps.pybo.models import Question


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


# 모델 등록
admin.site.register(Question, QuestionAdmin)
