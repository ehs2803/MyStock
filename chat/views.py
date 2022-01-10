import json

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.safestring import mark_safe


def landing(request):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))

    context = {
        'user': user
    }
    return render(request, "chat/chatIndex.html", context=context)

def room(request, room_name):
    user = None
    if request.session.get('id'):
        user = User.objects.get(id=request.session.get('id'))
    else:
        return redirect(f'/accounts')

    context = {
        'user': user,
        'username_json' : mark_safe(json.dumps(user.username)),
        'room_name_json': mark_safe(json.dumps(room_name))
    }
    return render(request, 'chat/room.html', context=context)