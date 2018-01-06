import datetime

import os
import json
from django.shortcuts import render
from shimons.models import DashboardPost, Request, DetectionAlgorithm, RequestAttachPattern, AnalysisResult, TagetCode
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from shimons.forms import RequestForm
from shimons.addons import compare


def save_file(file, path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


@login_required()
def dashboard(request):
    print(request)
    if request.GET.get('errors-field'):
        error = {request.GET.get('errors-field'): request.GET.get('errors_text')}
    else:
        error = None
    posts = DashboardPost.objects.all()
    pattern_form = RequestForm()
    reqs = Request.objects.filter(user=request.user.id)
    req_chart_data = []
    patterns_list = []
    tp_list = []
    tp_fn_list = []
    for req in reqs:
        if req.request_exe_status == "Done":
            analysis = AnalysisResult.objects.filter(request=req.request_id)
            for anal in analysis:  #:D
                targetCode = TagetCode.objects.get(targetcode_id=anal.targetcode_id)
                print(targetCode)
                result_path = os.path.join("user_" + str(request.user.id), "req_" + str(req.request_id),
                                           'reults', 'analysis_' + str(anal.request_id) + '_' + str(anal.targetcode_id),
                                           )
                print(anal.detectionresult_path, targetCode.patternsinfo_path)
                compare.compare_patterns(anal.detectionresult_path, targetCode.patternsinfo_path, result_path)
                anal.analysisresult_path = os.path.join(result_path, 'data.json')
                anal.save()
                with open(anal.analysisresult_path, 'r') as json_file:
                    data = json.load(json_file)
                    for key in data:
                        if key != "overall":
                            if key not in patterns_list:
                                patterns_list.append(key)
                                tp_list.append(data[key]['tp'])
                                tp_fn_list.append(data[key]['tp'] + data[key]['fn'])
                            else:
                                ind = patterns_list.index(key)
                                tp_list[ind] = tp_list[ind] + data[key]['tp']
                                tp_fn_list[ind] = tp_fn_list[ind] + data[key]['tp'] + data[key]['fn']
        req_chart_data.append({'tps': tp_list, "tpfns": tp_fn_list, "patterns_labels": patterns_list,
                               "status": req.request_exe_status})
    return render(request, 'sqlab/dashboard.html',
                  {'posts': posts, 'errors': error, 'req_form': pattern_form, 'reqs': reqs,
                   'chart_data': req_chart_data})


@login_required()
def upload_algorithm(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            main_file = form.cleaned_data.get('main')
            if not main_file.endswith('.jar'):
                main_file = main_file + '.jar'

            for file in request.FILES.getlist('jar_files'):
                # Check if files are not .jar files
                if not file.name.endswith('.jar'):
                    return HttpResponseRedirect(
                        '/dashboard/?errors-field=jar_files&errors_text=Please upload java executable files ('
                        '.jar)#upload')

                # Check main file exists in the files
                if main_file not in file.name:
                    error = {'jar-files-main': 'Your main file did not exist in uploaded files, try again.'}
                    return HttpResponseRedirect(
                        '/dashboard/?errors-field=jar_files_main&errors_text=Your main file did not exist in '
                        'uploaded '
                        'files, try again.#upload')

            req = Request()
            req.user_id = request.user.id
            req.request_date = datetime.datetime.now()
            req.save()
            alg_path = os.path.join("user_" + str(request.user.id), "req_" + str(req.request_id), 'Detection Algorithm',
                                    'jars')
            for file in request.FILES.getlist('jar_files'):
                save_file(file, alg_path)
            src_path = os.path.join("user_" + str(request.user.id), "req_" + str(req.request_id), 'Detection Algorithm',
                                    'src')
            for file in request.FILES.getlist('src_files'):
                save_file(file, src_path)
            pat_path = os.path.join("user_" + str(request.user.id), "req_" + str(req.request_id), 'Attached Patterns')
            for file in request.FILES.getlist('pattern_files'):
                save_file(file, pat_path)
            alg = DetectionAlgorithm()
            alg.request = req
            alg.jar_path = alg_path
            alg.main_jarFile = main_file
            alg.save()
            pattern = RequestAttachPattern()
            pattern.request = req
            pattern.patterns_dir = pat_path
            pattern.save()
            return HttpResponseRedirect('/dashboard/')

    return HttpResponseRedirect('/dashboard/')
