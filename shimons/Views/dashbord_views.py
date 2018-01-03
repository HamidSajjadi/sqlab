import datetime

import os
from django.shortcuts import render, redirect
from shimons.models import DashboardPost, RequestModel, Algorithm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse


def save_algorithm(file, path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


@login_required()
def dashbord(request):
    if request.GET.get('errors-field'):
        error = {request.GET.get('errors-field'): request.GET.get('errors-text')}
    else:
        error = None
    posts = DashboardPost.objects.all()
    return render(request, 'sqlab/dashbord.html', {'posts': posts, 'errors': error})


@login_required()
def upload_algorithm(request):
    if request.method == 'POST':
        main_file = request.POST.get('jar-files-main')
        # for file in request.FILES.getlist('jar-files'):
        #     if main_file not in file.name:
        #         error = {'jar-files-main': 'Your main file did not exist in uploaded files, try again.'}
        #         return HttpResponseRedirect(
        #             '/dashbord/?errors-field=jar-files-main&errors-text=Your main file did not exist in uploaded '
        #             'files, try again')
        #     if not file.name.endswith('.jar'):
        #         error = {'jar-files': 'Please upload jars'}
        #         return HttpResponseRedirect('/dashbord/?errors-field=jar-files&errors-text=Please upload jars')
        #
        req = RequestModel()
        req.user = request.user
        req.date = datetime.datetime.now()
        req.save()
        path = os.path.join("user_" + str(request.user.id), "req_" + str(req.id), 'detection algorithm')
        for file in request.FILES.getlist('jar-files'):
            save_algorithm(file, path)

        alg = Algorithm()
        alg.request = req
        alg.jar_path = path
        alg.main_jarFile = main_file
        alg.save()
        return HttpResponseRedirect('/dashbord/')

    return None
