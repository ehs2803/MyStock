from django.contrib.auth.models import User
from django.shortcuts import render
# Create your views here.

def landing(request):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "article/articleIndex.html", context=context)

def SE005930(request):
    # 사용자정보 로드
    user = None
    if request.session.get('id'):  # 로그인 중이면
        user = User.objects.get(pk=request.session.get('id'))  # 사용자 정보 저장

    # 페이지정보 로드
    all_freeboard_posts = BoardSe005930.objects.all().order_by('-id')  # 모든 자유게시판 데이터를 id순으로 가져오기
    paginator = Paginator(all_freeboard_posts, 10)  # 한 페이지에 10개씩 정렬
    page = int(request.GET.get('p', 1))  # p번 페이지 값, p값 없으면 1 반환
    posts = paginator.get_page(page)  # p번 페이지 가져오기

    # 자유 게시판 페이지(freeboard.html) 리턴
    return render(request, "board/SE005930/list.html",
                  {'posts': posts, 'user': user})

