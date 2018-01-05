import datetime

import os
from django.shortcuts import render
from shimons.models import DashboardPost, Request, DetectionAlgorithm, RequestAttachPattern
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
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
    pattern_form.fields['request'].queryset = Request.objects.filter(user=request.user)
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
        req = Request()
        req.user_id = request.user.id
        req.request_date = datetime.datetime.now()
        print("req: ",req)
        req.save()
        path = os.path.join("user_" + str(request.user.id), "req_" + str(req.request_id), 'Detection Algorithm', 'jars')
        for file in request.FILES.getlist('jar-files'):
            save_file(file, path)

        alg = DetectionAlgorithm()
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
            path = os.path.join("user_" + str(request.user.id), "req_" + str(req.request_id), 'Attached Patterns')
            for file in request.FILES.getlist('files'):
                save_file(file, path)
            pattern = RequestAttachPattern()
            pattern.request = req
            pattern.patterns_dir = path
            pattern.save()
            return HttpResponseRedirect('/dashbord/')
