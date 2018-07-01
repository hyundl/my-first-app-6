from django.shortcuts import render
from .forms import *
from django.contrib.auth import login, authenticate
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse

def signup(request):
    # 처음 왔을 땐 GET방식, 회원가입하고 제출 누르면 POST방식
    if request.method == "GET":
        form = UserForm()
        return render(request, "customlogin/templates/signup.html", {'form':form}) 
        # 왼쪽은 문자열, 오른쪽은 위에 만든 객체
    elif request.method == "POST":
        form = UserForm(request.POST) # 사용자가 입력한 정보 POST에 담겨있으니까 넘겨줘야해
        if form.is_valid(): # 유효한 값이 다 들어있는지 빈칸이 없는지 확인
            
            # 패스워드 확인
            if form.cleaned_data['password'] == form.cleaned_data['password_check']:
                
                #new_user = User.objects.create_user(**form.cleaned_data)
                
                # ** 두개 붙으면 딕셔너리 형태로 다양한 데이터를 처리할 수 있음 / * 리스트 형태로 처리 
                # form.cleaned_data : 폼객체에 저장된 값들을 꺼낼 때 사용(사전형)
                # def func1(q,b,**a) : **a : q,b 매개변수 외에 다른 값들이 들어오면 사전형으로 a변수가 처리 
                
                # create_user : 값들이 들어오면 user만들어주는 함수 
                # create_user(username=form.cleaned_data['username'],
                #             password=form.cleaned_data['password'],
                #             email=form.cleaned_data['email'])
                # create_user(username,password,email) : 장고에서 지원하는 User 모델클래스에 새로운 객체를 만들 때 사용
                # 다만 매개변수 이름과 키값이 같아야만 저절로 넣어줄 수 있다. 다르다면 하나씩 꺼내서 넣어주기
                
                # User 모델클래스는 'password_check' 속성을 사용하지 않아 에러 발생 
                new_user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password'])
                
                login(request, new_user)
                # login(request, User 객체) : 해당 요청을 보낸 클라이언트가 User객체로 로그인하는 작업을 함
                
                return HttpResponseRedirect(reverse('vote:index'))
                # reverse : 별칭을 가진 url로 매칭시켜주는 역할(엄밀히 따지면 view불러줌)
                # 다른 url 전송해줘서 클라이언트가 다시 그 url로 요청을 할 수 있도록
                # HTML파일 부르는건 render 
                
            else:
                error = "비밀번호가 맞지않음"
                
        else:
            error = "유효하지않은 값이 입력됨"
            
        return render(request, "customlogin/templates/signup.html", {'form':form, 'error':error})

    #
    
def signin(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "customlogin/templates/signin.html", {'form':form})
    elif request.method == "POST":
        form = LoginForm(request.POST) # ID,PW 실패시 보낼 폼 
        #if form.is_valid():
        username1 = request.POST.get('username')#form.cleaned_data['username']
        password1 = request.POST.get('password')#form.cleaned_data['password']
        
        # 로그인하려면 해당되는 유저 객체를 찾아야해
        user = authenticate(username=username1, password=password1)
        # authenticate(username,password) : User 모델클래스에 해당 ID와 PW로 저장된 객체를 찾아 반환
        #                                   객체가 없는 경우 None 반환(ID가 없거나 ID있는데 PW가 없거나)
        #                                   왼쪽 - 함수내에서 사용하는 매개변수 이름/오른쪽 - 꺼내온거 
        
        if user is not None:
        # (값,변수) is 타입 : (값,변수)가 타입과 동일한지 True,False반환
        # user변수의 값이 None타입이 아닌가?
        # user is not None == not(user is None) 
            login(request, user)
            return HttpResponseRedirect(reverse("vote:index"))
        else: # 해당 ID와 PW를 가진 User객체가 없는 경우
            error = "ID 또는 PW가 틀렸습니다"
        
        #else:
        #    error = "유효하지않은 데이터입니다"
            
        return render(request, "customlogin/templates/signin.html", {'form':form, 'error':error})














