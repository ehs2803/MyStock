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
    return render(request, "board/boardIndex.html", context=context)
    '''
    return render(
        request,
        'single/index.html',
    )
    '''

def SE005930(request):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "board/SE005930/list.html", context=context)