from django.contrib.auth.models import User
from django.shortcuts import render

from bs4 import BeautifulSoup
import requests
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

    search='삼성전자'
    page_num=1
    # url 생성
    url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(page_num)

    # html불러오기
    original_html = requests.get(url)
    html = BeautifulSoup(original_html.text, "html.parser")

    # 검색결과
    articles = html.select("div.group_news > ul.list_news > li div.news_area > a")

    # 뉴스기사 제목 가져오기
    news_title = []
    for i in articles:
        news_title.append(i.attrs['title'])

    # 뉴스기사 URL 가져오기
    news_url = []
    for i in articles:
        news_url.append(i.attrs['href'])

    news = []
    for i, _ in enumerate(news_title):
        news_dict={}
        news_dict['title']=news_title[i]
        news_dict['url']=news_url[i]
        news.append(news_dict)
    #  리턴
    return render(request, "article/articles.html",
                  {'title': search, 'news':news, 'user': user})

