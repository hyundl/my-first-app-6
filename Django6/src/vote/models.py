from django.db import models
from django.contrib.auth.models import User # 장고가 생성한 User 모델클래스 

# 모델 : 데이터를 어떤 형식으로 저장할지 표현하는 것
# 모델 클래스 정의 후 객체를 만들어 사용
# class 클래스명(models.Model)
# 모델 정의를 다한 후 해야하는 행동
# - 모델클래스가 변경된 애플리케이션에서 MakeMigration
#   - 프로젝트 우클릭 -> dJango -> make migration 선택 -> 애플리케이션이름 입력 
# - 변경사항을 데이터베이스에 적용 -> Migrate
#   - 프로젝트 우클릭 -> dJango -> migrate 선택
# MakeMigration , Migrate 시 settings.py -> INSTALLED_APPS 변수에 애플리케이션 이름이 들어가있어야함!!

class Question(models.Model):
    
    # User 모델클래스를 외래키로 참조 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    question_text = models.CharField('질문 제목', max_length=200) #
    # models.CharField : 글자수 제한이 있는 문자열 저장시 사용
    
    pub_date = models.DateTimeField('생성일자')
    # models.DateTimeField : 날짜 시간을 저장시 사용
    
    #
    
    def __str__(self):
        return self.question_text
    # str : 각 객체를 문자열로 표현할 때 호출
    
    #
    
class Choice(models.Model):
    choice_text = models.CharField('답변 제목', max_length=100)
    votes = models.IntegerField('투표 수', default=0) 
    # IntegerField : 정수값을 저장할 수 있는 클래스 
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ForeignKey : 외래키. 다른 테이블을 참조
    # Question 객체 1개 : Choice 객체 n개
    # on_delete : 연결한 객체가 삭제됐을 때 자신도 삭제될지 옵션을 지정
    def __str__(self):
        return self.choice_text
    
    
    
    
    
    
    
    
    
    
    