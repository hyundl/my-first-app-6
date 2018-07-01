from django.urls import path
from .views import *

app_name = 'Blog'

urlpatterns=[
    path('', index.as_view(), name='index'),
    # 함수 기반이 아니라 클래스 기반이기 때문에
    # 클래스뷰.as_view() : 클래스뷰가 URL 매칭시 사용
    path('<int:post_id>/', detail, name='detail'),
    path('posting/', posting, name='posting'),
    path('search/', searchP, name='searchP')
    ]