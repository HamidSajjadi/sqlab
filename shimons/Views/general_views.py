from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from shimons.models import Post


def index(request):
    # if request.user.is_authenticated:
    #     return HttpResponse("okay")
    # else:
    #     return HttpResponse("nope")

    posts = Post.objects.filter(status=1)
    return render(request, 'sqlab/index.html', {'posts': posts})
