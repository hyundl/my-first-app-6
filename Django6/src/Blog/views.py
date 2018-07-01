from django.shortcuts import render, get_object_or_404

from django.views.generic.list import ListView
# generic 뷰 : 장고에서 제공하는 여러가지 기능으로 나눈 뷰 클래스 
from .models import *
from .forms import *
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# 클래스 기반의 뷰
# class 뷰이름(기능별 뷰 클래스):
# ListView : 특정 객체의 목록을 다루는 기능을 가진 뷰 클래스

class index(ListView):
    template_name = "Blog/templates/index.html"
    # template_name='' : HTML파일 문자열을 넣음
    model = Post
    # model : 모델클래스명을 입력
    context_object_name = 'list'
    # context_object_name : 템플릿에서 사용할 객체 리스트의 변수명
    paginate_by = 5
    # paginate_by : 한 페이지에 몇개의 객체가 보일지 숫자를 입력
    
def detail(request, post_id):
    obj = get_object_or_404(Post, pk=post_id)
    return render(request, 'Blog/templates/detail.html',{'post':obj})

@login_required
def posting(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "Blog/templates/posting.html", {'form':form})
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)   
            # 글쓴이를 저장하는 변수가 빈공간이므로 바로 데이터베이스에 저장하지 않고 Post객체로 변환
            obj.author = request.user
            # 요청한 클라이언트 유저와 매칭
            obj.save()
            # 객체를 데이터베이스에 저장
            
            # request.FILES : 클라이언트가 보낸 파일들에 대한 데이터
            # Image 객체 생성 및 저장
            # HTML 폼에서 name이 images로 지정된 파일을 추출
            for f in request.FILES.getlist('images'):
                image = Image(post=obj, image=f)
                # Image 객체 생성
                image.save()
                # DB에 저장
            # File 객체 생성 및 저장
            for f in request.FILES.getlist('files'):
                file = File(post=obj, file=f)
                file.save()
                
            # 글에 대한 처리는 폼에서, 파일과 이미지는 for문에서 처리
            
            return HttpResponseRedirect(reverse('Blog:detail', args=(obj.id,)))
        
def searchP(request):
    # 보통 검색을 하는 방식은 GET방식
    q = request.GET.get('q', '')    
    # q라는 이름, GET방식으로 들어온 내용 추출, 기본값
    type = request.GET.get('type','0')
    
    # type : '0' 제목 검색 
    if type == '0':
        
        list = Post.objects.filter(headline__contains=q)
        # 모델클래스.objects.filter() : 특정 조건을 만족하는 모든 객체 추출
        # filter,get,exclude에 조건을 넣을 때 (모델클래스의 변수__명령어=값) 형태로 넣음
        # contains : 우변 값이 해당 변수에 포함되어있는 객체를 모두 추출
        # 아직까지는 데이터베이스에 접근한거 아님
        
        return render(request, "Blog/templates/searchP.html", {'list':list})
        
    # type : '1' 글쓴이 검색
    elif type == '1':
        
        # 해당하는 글쓴이가 있는지 없는지부터 확인
        user = User.objects.get(username=q)
        list = Post.objects.filter(author=user)
        return render(request, "Blog/templates/searchP.html", {'list':list})
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
        
        
        
        
        
        
        
        
        
        
        
        