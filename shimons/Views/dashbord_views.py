from django.shortcuts import render
from shimons.models import DashboardPost
from django.contrib.auth.decorators import login_required


@login_required()
def dashbord(request):
    posts = DashboardPost.objects.all()
    return render(request, 'sqlab/dashbord.html', {'posts': posts})
