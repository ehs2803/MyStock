from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from accounts.models import AuthUser
from board.models import BoardSe005930, CommentSe005930
from datetime import datetime
from django.utils import timezone

def landing(request):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "board/boardIndex.html", context=context)
    '''
    return render(
        request,
        'single/index.html',
    )
    '''

def SE005930(request):
    # 사용자정보 로드
    user = None
    if request.session.get('id'):                                 # 로그인 중이면
        user = User.objects.get(pk=request.session.get('id'))     # 사용자 정보 저장

    # 페이지정보 로드
    all_freeboard_posts = BoardSe005930.objects.all().order_by('-id')       # 모든 자유게시판 데이터를 id순으로 가져오기
    paginator = Paginator(all_freeboard_posts, 10)                      # 한 페이지에 10개씩 정렬
    page = int(request.GET.get('p', 1))                                 # p번 페이지 값, p값 없으면 1 반환
    posts = paginator.get_page(page)                                    # p번 페이지 가져오기

    # 자유 게시판 페이지(freeboard.html) 리턴
    return render(request, "board/SE005930/list.html",
                  {'posts': posts, 'user': user})



def board_SE005930_writing(request):
    # 사용자정보 로드
    user = None
    if request.session.get('id'):                                     # 로그인 중이면
        user = AuthUser.objects.get(pk=request.session.get('id'))       # 사용자 정보 저장
    # POST 요청시
    if request.method =='POST':
        # 새 게시글 객체 생성
        new_post = BoardSe005930.objects.create(
            title=request.POST['title'],
            contents=request.POST['contents'],
            uid=user,
            username=user.username
        )
        return redirect(f'/board/SE005930/post/{new_post.id}')               # 해당 게시글 페이지로 이동

    # GET 요청시 글쓰기 페이지(writing.html) 리턴
    return render(request, 'board/SE005930/board_writing.html', {'user' : user})

# Free Board 게시글 보기
def board_SE005930_post(request, pk):
    # 사용자정보 로드
    user = None
    uname = None
    if request.session.get('id'):                                     # 로그인 중이면
        user = User.objects.get(pk=request.session.get('id'))     # 사용자 정보 저장
        uname = user.username

    # 게시글 정보 로드
    post = get_object_or_404(BoardSe005930, pk=pk)
    # 댓글 정보 로드
    comment = CommentSe005930.objects.filter(pid=pk).order_by('created_date')

    # 해당 게시글 페이지(freeboard_post.html) 반환
    return render(request, 'board/SE005930/board_post.html',
                  {'post' : post, 'user' : user, 'uname':uname,'comment':comment})

# Free Board 게시글 수정
def board_SE005930_edit(request, pk):
    # 사용자정보 로드
    user = None
    if request.session.get('id'):                                     # 로그인 중이면
        user = User.objects.get(pk=request.session.get('id'))     # 사용자 정보 저장

    # 게시글 정보 로드
    post = BoardSe005930.objects.get(pk=pk)

    # POST 요청시
    if request.method == "POST":
        post.title = request.POST['title']                              # 제목 수정 반영
        post.contents = request.POST['contents']                        # 내용 수정 반영
        post.save()                                                     # 수정된 내용 저장
        return redirect(f'/board/SE005930/post/{pk}')                        # 해당 게시글 페이지로 이동

    # GET 요청시 게시글 수정 페이지(postedit.html) 리턴
    return render(request, 'board/SE005930/board_edit.html', {'post':post, 'user' : user})

# Free Board 게시글 삭제
def board_SE005930_delete(request, pk):
    post = BoardSe005930.objects.get(id=pk)                                 # 해당 게시글 테이블 저장
    post.delete()                  # 해당 게시글 삭제
    return redirect(f'/board/SE005930')     # 자유 게시판 페이지로 이동


def board_SE005930_comment(request, pk):
    post = get_object_or_404(BoardSe005930, pk=pk)
    # 사용자정보 로드
    user = None
    if request.session.get('id'):  # 로그인 중이면
        user = AuthUser.objects.get(pk=request.session.get('id'))  # 사용자 이름 저장

    # POST 요청시
    if request.method == 'POST':
        new_comment = CommentSe005930.objects.create(
            pid=BoardSe005930.objects.get(id=pk),
            uid=user.id,
            username=user.username,
            comments=request.POST['content'],
        )
        return redirect(f'/board/SE005930/post/{post.id}',{'post': post, 'user': user})  # 해당 게시글 페이지로 이동

    return render(request, f'/board/SE005930/post/{post.id}',{'post': post, 'user': user})

# Free Board 게시글 삭제
def comment_SE005930_delete(request, pk, date):
    post = get_object_or_404(BoardSe005930, pk=pk)
    # Jan. 3, 2022, 9:41 a.m.
    timelist = date.split(' ')
    year = timelist[2][0:4]
    month = '01' #timelist[0][:timelist[0].find(',')]
    day = timelist[1][:timelist[1].find(',')]
    hour = timelist[3][:timelist[3].find(':')]
    if timelist[4][0]=='p':
        if hour!='12': hour = int(hour)+12
    min = timelist[3][timelist[3].find(':')+1:]
    hour='5'
    #YYYY - MM - DD HH: MM
    # 사용자정보 로드
    user = None
    if request.session.get('id'):  # 로그인 중이면
        user = AuthUser.objects.get(pk=request.session.get('id'))  # 사용자 이름 저장

    print(year, month, day, hour, min)
    comment = CommentSe005930.objects.filter(pid=pk, uid=user.id)
    for i in comment:
        time = str(i.created_date)
        timesplit = time.split(' ')
        temp_date = timesplit[0].split('-')
        temp_time = timesplit[1].split(':')
        cyear = temp_date[0]
        cmonth = temp_date[1]
        cday = temp_date[2]
        chour = temp_time[0]
        cmin = temp_time[1]
        print(cyear, cmonth, cday, chour, cmin)
        if int(year)==int(cyear) and int(month)==int(cmonth) and int(day)==int(cday) and int(hour)==int(chour) and int(min)==int(cmin):
            i.delete()
            break
    return redirect(f'/board/SE005930/post/{post.id}')     # 자유 게시판 페이지로 이동

