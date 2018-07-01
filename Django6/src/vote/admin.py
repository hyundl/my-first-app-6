from django.contrib import admin
from .models import Question, Choice

class ChoiceAdmin(admin.ModelAdmin):
# 관리자 페이지에서 효과적으로 객체 정보를 볼수 있는 ModelAdmin클래스 상속
    #fields = ['choice_text', 'votes', 'question']
    fields = ['choice_text', 'question']
    #list_display = ('choice_text', 'votes')
    list_display = ('choice_text', 'votes', 'question')

# admin.py : 관리자 사이트에서 모델클래스를 조회,삽입,삭제,수정하고자 할 때 설정하는 파이썬파일
# admin.site.register(클래스명)
# 해당 모델클래스를 관리자사이트에 등록
# 해당 파일에서 모델클래스를 알아야되므로 from ~ import를 사용 

admin.site.register(Question) # Question 모델클래스를 관리자 사이트에서 접근할 수 있도록 설정

#admin.site.register(Choice) # Choice 모델클래스를 관리자 사이트에서 접근할 수 있도록 설정
admin.site.register(Choice, ChoiceAdmin)


