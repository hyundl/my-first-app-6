from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# reverse(문자열, args=튜플)
# 문자열에 해당하는 URL별칭을 찾고, 매개변수가 필요한 URL일 경우 args 매개변수에 있는 튜플값으로 자동 매핑
from .models import Question, Choice
from django.http.response import HttpResponseRedirect

import datetime # 파이썬 내장모듈, 시간정보를 얻을 때 사용

from .forms import * # QuestionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from . import forms # forms.QuestionForm

# �Լ� or Ŭ����

# views.py : 내부적으로 동작할 행동들을 정의
# HTML 파일 전달,검색,등록,삭제,수정
# 함수 or 클래스 형태로 뷰 구현
# 함수형태로 구현시 반드시 첫번째 매개변수로 request 사용
# request : 웹 클라이언트의 요청에 대한 정보를 담고 있는 변수

def index(request):
    print("index")
    
    # 1.Question ��ü ã��
    list = Question.objects.all() # ����� �޾��� ����
    # ?.objects.all() : Question 모델 클래스에 저장된 모든 객체 추출
    
    # 2.���ø�(HTML)�� ���� �����ϱ�
    return render(request, "vote/templates/index.html", {'question_list':list})
    # render(request, HTML 파일경로, HTML���Ͽ� ������ ������-������)
    
    #
    
def detail(request, question_id):
    p = get_object_or_404(Question, pk = question_id)
    # get_object_or_404 : 모델클래스에 id값으로 객체 1개를 반환하는 함수
    # 만약 객체를 못찾는 경우 클라이언트에게 404에러 메시지를 전달
    # primary key 
    return render(request, "vote/templates/detail.html", {'question':p})

    #
    
def vote(request, question_id): # 얘를 받는 이유 : 결과창을 보여주기 위해
    if request.method == "POST":
    # request.method : 클라이언트의 요청 방식이 저장된 변수
    # "GET", "POST" 문자열 비교. 대소문자 구분
        id = request.POST.get('choice') # detail에서 name
        # request.POST : POST방식으로 들어온 데이터들
        # request.POST.get(문자열) : POST방식으로 들어온 데이터 중 name속성의 값이 문자열과 같은 데이터를 추출
        # get 함수가 반환하는 데이터는 무조건 문자열 
        obj = get_object_or_404(Choice, pk=id)
        obj.votes += 1
        obj.save() # 모델클래스의 객체.save() : 변동사항을 저장 
        
        #return HttpResponseRedirect(reverse('result', args=(question_id,)))
        return HttpResponseRedirect(reverse('vote:result', args=(question_id,)))
        # 튜플을 만들 때 요소 개수가 한개면 사칙연산에 사용하는 우선순위 괄호로 판단하기 떄문에 
        # 튜플 요소 개수가 한개일 경우 끝에 쉼표를 입력
        
        #return redirect('/result/%s/' %(question_id))
        # redirect(문자열) : 문자열에 해당하는 URL주소로 변경
        # 내부적으로 연산하고 다른 URL로 토스하기 때문에 template를 만들 필요가 없음
    
    #
    
def result(request, question_id):
    data = Question.objects.get(id=question_id)
    # 모델클래스.objects.get(조건) : 조건에 맞는 객체를 1개 찾아 반환
    return render(request, "vote/templates/result.html", {'obj':data})
    
    #

# 뷰 함수 정의시 위에 @함수명 작성하면, 해당 뷰를 호출하기 전에 함수명에 해당하는 함수가 먼저 호출됨
@login_required
def registerQ(request):
    if request.method == "GET":
        form = QuestionForm() # QuestionForm 객체 생성, 사용하는 속성들이 공란으로 되어있음
        return render(request, "vote/templates/registerQ.html", {'form':form}) # 원래 {} 
    elif request.method == "POST":
        #name = request.POST.get('question_text')
        #obj = Question()
        #obj.question_text = name
        
        form = QuestionForm(request.POST)
        if form.is_valid(): # 폼객체.is_valid() : 해당 폼에 입력값들이 에러가 없는지 확인. True False 값 반환
                            #                   폼 객체 사용시 반드시 사용해야하는 함수
            obj = form.save(commit=False) 
            # 폼객체.save() : 해당 폼에 입력값들로 모델클래스 객체를 데이터베이스에 저장 후 반환
            # 폼객체.save(commit=False) : 데이터베이스에 바로 저장하지 않고 
            #                           모델폼에서 모델클래스 객체로 변환 후 반환
            
            user = User.objects.get(username=request.user.get_username())
            # request.user.get_username() : 로그인된 회원의 username을 반환하는 함수 
        
            obj.pub_date = datetime.datetime.now()
            
            obj.author = user
            
            obj.save()
            return HttpResponseRedirect(reverse('vote:detail', args=(obj.id,)))
        else: # 입력 양식에 문자가 있을 경우의 처리 
            return render(request, "vote/templates/registerQ.html", {'form':form, 'error':"입력이 잘못됐습니다."})
            # 템플릿으로 form 전달하면 사용자가 이전에 작성한 내용이 들어있는 상태로 전달함
    
    #
    
@login_required
def deleteQ(request, question_id):
    obj = get_object_or_404(Question, pk=question_id) # pk = id
    
    if obj.author.username != request.user.get_username():
        return render(request, "vote/templates/error.html", 
                      {'error':"잘못된 접근입니다", 'returnURL':reverse('vote:detail', args=(question_id,))})
    
    obj.delete() # 해당 객체를 데이터베이스에서 삭제
    return HttpResponseRedirect(reverse('vote:index'))
    
    #
    
def registerC(request,question_id):
    
    obj = get_object_or_404(Question, pk=question_id)
    if request.user.get_username() != obj.author.username:
        return render(request, "vote/templates/error.html", 
                      {'error':"본인이 작성한 글이 아닙니다", 'returnURL':reverse('vote:detail', args=(question_id,))})
    
    if request.method == "GET":
        # Choice 폼 객체 생성
        form = ChoiceForm()
        # render 함수로 HTML파일 로드 + 템플릿에 폼객체 전달(뷰 코드 작성 및 HTML파일 생성까지)
        return render(request, "vote/templates/registerC.html", {'form':form, 'name':obj.question_text})
        
    elif request.method == "POST":
        # 폼객체 생성(클라이언트의 데이터를 넣음)
        form = ChoiceForm(request.POST)
        # 폼의 에러 확인
        if form.is_valid():
            # 모델클래스 객체를 데이터베이스에 저장 및 반환
            obj1 = form.save(commit=False)
            
            obj1.question = obj
            obj1.save()
            
            return HttpResponseRedirect(reverse('vote:detail', args=(obj1.question.id, )))
        else:
            return render(request, "vote/templates/registerC.html", 
                          {'form':form, 'error':"입력 오류", 'name':obj.question_text})
        # 다른페이지로 전달
        # 에러 전달
        
@login_required
def deleteC(request, choice_id):
    # 1. 뷰 구현 - deleteQ 함수 참고
    # Choice 객체 찾기
    obj = get_object_or_404(Choice, pk=choice_id)
    
    if request.user.get_username() != obj.question.author.username:
        return render(request, "vote/templates/error.html", 
                      {'error':"잘못된 접근입니다", 'returnURL':reverse('vote:detail', args=(obj.question.id,))})
    
    id = obj.question.id # choice 객체 삭제 전에 Question 객체의 id값을 저장
    obj.delete()
    # detail or index 페이지로 이동
    return HttpResponseRedirect(reverse('vote:detail', args=(id,)))
    # 2. urls 등록 - vote/urls.py에서 수정
    # 3. detail.html 파일 수정 - vote/templates/detail.html
    # 각 답변 항목별로 '삭제'링크 만들기
    
    #
    
@login_required
def updateQ(request, question_id):
    obj = get_object_or_404(Question, pk=question_id)
    
    if request.user.get_username() != obj.author.username:
    # obj.author 해당 Question객체를 작성한 User객체
    # 해당 질문을 쓴 글쓴이 이름과 로그인된 유저의 이름을 비교
        return render(request, "vote/templates/error.html", 
                      {'error':"본인이 작성한 글이 아닙니다", 'returnURL':reverse('vote:detail', args=(question_id,))})
    
    if request.method == "GET":
        form = QuestionForm(instance = obj)
        # Question 객체에 저장된 값을 QuestionForm 객체를 생성할 때 입력
        # 모델폼의 생성자에 instance 매개변수는 이미 생성된 모델클래스의 객체를 담을 수 있음
        return render(request, "vote/templates/updateQ.html", {'form':form})
    elif request.method == "POST":
        form = QuestionForm(request.POST, instance=obj)
        # 이미 생성된 Question 객체에 내용을 클라이언트가 작성한 내용으로 덮어씌움
        if form.is_valid():
            question = form.save(commit=False) # 더 입력을 해야하는 공간이 남아있을 때 
            question.pub_date = datetime.datetime.now()
            question.save()
            return HttpResponseRedirect(reverse('vote:detail', args=(question_id,)))
        else:
            return render(request, "vote/templates/updateQ.html", {'form':form, 'error':"유효하지 않은 데이터"})
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   
   
    