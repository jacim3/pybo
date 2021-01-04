from django import template

register = template.Library()


# 해당 어노테이션을 붙이면, 템플릿에서 해당 함수를 필터로 사용하도록 허용
@register.filter
def sub(value, arg):
    return value - arg
