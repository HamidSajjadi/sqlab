import datetime

import os
from django.shortcuts import render, redirect
from shimons.models import DashboardPost, RequestModel, Algorithm, Patterns
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from shimons.forms import PatternForm


def save_file(file, path):
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
    pattern_form = PatternForm()
    pattern_form.fields['request'].queryset = RequestModel.objects.filter(user=request.user)
    print(RequestModel.objects.filter(user=request.user))
    return render(request, 'sqlab/dashbord.html', {'posts': posts, 'errors': error, 'pattern_form': pattern_form})


@login_required()
def upload_algorithm(request):
    if request.method == 'POST':
        main_file = request.POST.get('jar-files-main')
        name = request.POST.get('name')
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
        req.name = name
        req.date = datetime.datetime.now()
        req.save()
        path = os.path.join("user_" + str(request.user.id), "req_" + str(req.id), 'Detection Algorithm', 'jars')
        for file in request.FILES.getlist('jar-files'):
            save_file(file, path)

        alg = Algorithm()
        alg.request = req
        alg.jar_path = path
        alg.main_jarFile = main_file
        alg.save()
        return HttpResponseRedirect('/dashbord/')

    return HttpResponseRedirect('/dashbord/')


def upload_patterns(request):
    if request.method == 'POST':
        form = PatternForm(request.POST, request.FILES)
        if form.is_valid():
            req = form.cleaned_data['request']
            path = os.path.join("user_" + str(request.user.id), "req_" + str(req.id), 'Attached Patterns')
            print("file11: ", request.FILES.getlist('files'))
            for file in request.FILES.getlist('files'):
                save_file(file, path)
            pattern = Patterns()
            pattern.request = req
            pattern.pattern_path = path
            pattern.save()
            return HttpResponseRedirect('/dashbord/')
