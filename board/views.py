from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import models
from urllib import parse
from ast import literal_eval
import requests
# Create your views here.
from accounts.models import AuthUser

from datetime import datetime
from django.utils import timezone

from board.models import Board, Comment


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

def get_sise(code, start_time, end_time, time_from='day') :
    get_param = { 'symbol':code, 'requestType':1, 'startTime':start_time, 'endTime':end_time, 'timeframe':time_from }
    get_param = parse.urlencode(get_param)
    url="https://api.finance.naver.com/siseJson.naver?%s"%(get_param)
    response = requests.get(url)
    return literal_eval(response.text.strip())

def BOARD(request, code):

    info = get_sise('005930', '20210601', '20210605', 'day')
    print(info)
    # 사용자정보 로드
    user = None
    if request.session.get('id'):                                 # 로그인 중이면
        user = User.objects.get(pk=request.session.get('id'))     # 사용자 정보 저장

    # 페이지정보 로드
    all_freeboard_posts = Board.objects.filter(code=code) # all().order_by('-id')       # 모든 자유게시판 데이터를 id순으로 가져오기
    paginator = Paginator(all_freeboard_posts, 10)                      # 한 페이지에 10개씩 정렬
    page = int(request.GET.get('p', 1))                                 # p번 페이지 값, p값 없으면 1 반환
    posts = paginator.get_page(page)                                    # p번 페이지 가져오기
    code = code
    # 자유 게시판 페이지(freeboard.html) 리턴
    return render(request, "board/list.html",
                  {'posts': posts, 'user': user, 'code':code})

def BOARD_writing(request, code):
    # 사용자정보 로드
    user = None
    if request.session.get('id'):                                     # 로그인 중이면
        user = AuthUser.objects.get(pk=request.session.get('id'))       # 사용자 정보 저장
    # POST 요청시
    if request.method =='POST':
        # 새 게시글 객체 생성
        new_post = Board.objects.create(
            title=request.POST['title'],
            contents=request.POST['contents'],
            uid=user,
            username=user.username,
            code = code
        )
        return redirect(f'/board/{code}/post/{new_post.id}')               # 해당 게시글 페이지로 이동

    # GET 요청시 글쓰기 페이지(writing.html) 리턴
    return render(request, 'board/board_writing.html', {'user' : user, 'code':code})

def BOARD_post(request, pk, code):
    # 사용자정보 로드
    user = None
    uname = None
    code=code
    if request.session.get('id'):                                     # 로그인 중이면
        user = User.objects.get(pk=request.session.get('id'))     # 사용자 정보 저장
        uname = user.username

    # 게시글 정보 로드
    post = get_object_or_404(Board, pk=pk)
    # 댓글 정보 로드
    comment = Comment.objects.filter(pid=pk).order_by('created_date')

    # 해당 게시글 페이지(freeboard_post.html) 반환
    return render(request, 'board/board_post.html',
                  {'post' : post, 'user' : user, 'uname':uname,'comment':comment, 'code':code})

def BOARD_edit(request, pk, code):
    # 사용자정보 로드
    user = None
    if request.session.get('id'):                                     # 로그인 중이면
        user = User.objects.get(pk=request.session.get('id'))     # 사용자 정보 저장

    # 게시글 정보 로드
    post = Board.objects.get(pk=pk)

    # POST 요청시
    if request.method == "POST":
        post.title = request.POST['title']                              # 제목 수정 반영
        post.contents = request.POST['contents']                        # 내용 수정 반영
        post.save()                                                     # 수정된 내용 저장
        return redirect(f'/board/{code}/post/{pk}')                        # 해당 게시글 페이지로 이동

    # GET 요청시 게시글 수정 페이지(postedit.html) 리턴
    return render(request, 'board/board_edit.html', {'post':post, 'user' : user})

def BOARD_delete(request, pk, code):
    post = Board.objects.get(id=pk)                                 # 해당 게시글 테이블 저장
    post.delete()                  # 해당 게시글 삭제
    return redirect(f'/board/{code}')     # 자유 게시판 페이지로 이동

def BOARD_comment(request, pk, code):
    post = get_object_or_404(Board, pk=pk)
    # 사용자정보 로드
    user = None
    if request.session.get('id'):  # 로그인 중이면
        user = AuthUser.objects.get(pk=request.session.get('id'))  # 사용자 이름 저장

    # POST 요청시
    if request.method == 'POST':
        new_comment = Comment.objects.create(
            pid=Board.objects.get(id=pk),
            uid=user.id,
            username=user.username,
            comments=request.POST['content'],
        )
        return redirect(f'/board/{code}/post/{post.id}',{'post': post, 'user': user})  # 해당 게시글 페이지로 이동

    return render(request, f'/board/SE005930/post/{post.id}',{'post': post, 'user': user})


def BOARD_comment_delete(request, pk, ci, code):
    post = get_object_or_404(Board, pk=pk)
    user = None
    if request.session.get('id'):  # 로그인 중이면
        user = AuthUser.objects.get(pk=request.session.get('id'))  # 사용자 이름 저장

    comment = Comment.objects.filter(pid=pk, comment_id=ci)
    comment.delete()
    return redirect(f'/board/{code}/post/{post.id}',{'post': post, 'user': user})  # 해당 게시글 페이지로 이동
