import datetime

import os
import json
from django.shortcuts import render
from shimons.models import DashboardPost, Request, DetectionAlgorithm, RequestAttachPattern, AnalysisResult, TagetCode, \
    TargetCodeConfig, RequestSelectPattern
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


def proccess_analysis(request, req, final_file_path):
    analysis = AnalysisResult.objects.filter(request=req.request_id)
    file_set = {'simple': [], 'medium': [], 'hard': []}
    for anal in analysis:  #:D
        targetCode = TagetCode.objects.get(targetcode_id=anal.targetcode_id)
        complexity = TargetCodeConfig.objects.get(complexity_id=targetCode.complexity_id)
        result_path = os.path.join("user_" + str(request.user.id), "req_" + str(req.request_id),
                                   'results',
                                   'analysis_' + str(anal.request_id) + '_' + str(anal.targetcode_id),
                                   )
        compare.compare_patterns(anal.detectionresult_path, targetCode.patternsinfo_path, result_path,
                                 prefix=complexity.complexity_level)
        anal.analysisresult_path = os.path.join(result_path, complexity.complexity_level + '_data.json')
        file_set[complexity.complexity_level].append(anal.analysisresult_path)
        # return None
        anal.save()
    if len(file_set['simple']) > 0:
        compare.summarize(file_set['simple'], final_file_path, 'simple.json')
    if len(file_set['medium']) > 0:
        compare.summarize(file_set['medium'], final_file_path, 'medium.json')
    if len(file_set['hard']) > 0:
        compare.summarize(file_set['hard'], final_file_path, 'hard.json')


def proccess_chart_data(raw_data):
    tp_list = []
    tp_fn_list = []
    patterns_list = []
    overall = []
    for pattern in raw_data:
        if pattern == 'overall':
            overall = raw_data[pattern]
            continue
        patterns_list.append(pattern)
        tp_list.append(0)
        tp_fn_list.append(0)
        for instannce in raw_data[pattern]:
            tp_list[patterns_list.index(pattern)] += instannce['tp']
            tp_fn_list[patterns_list.index(pattern)] += (instannce['tp'] + instannce['fn'])
    return {'tp_list': tp_list, 'tp_fn_list': tp_fn_list, 'patterns_list': patterns_list, 'overall': overall,
            'len': len(patterns_list)}


def proccess_search_data(final_file_path):
    simple = {'fn': [], 'tp': [], 'fp': []}
    medium = {'fn': [], 'tp': [], 'fp': []}
    hard = {'fn': [], 'tp': [], 'fp': []}

    simple_file = os.path.join(final_file_path, 'simple.json')
    medium_file = os.path.join(final_file_path, 'medium.json')
    hard_file = os.path.join(final_file_path, 'hard.json')
    if os.path.isfile(simple_file):
        data = json.load(open(simple_file, 'r'))
        for pattern in data:
            if pattern == 'overall':
                continue
            simple['tp'].append({pattern: []})
            simple['fn'].append({pattern: []})
            simple['fp'].append({pattern: []})
            for instance in data[pattern]:
                if instance['tp'] > 0:
                    simple['tp'][len(simple['tp'])-1][pattern].append(
                        {"System result": instance['System result'], "User result": instance['User result']})
                if instance['fn'] > 0:
                    simple['fn'][len(simple['fn']) - 1][pattern].append(
                        {"System result": instance['System result'], "User result": instance['User result']})
                if instance['fp'] > 0:
                    simple['fp'][len(simple['fp']) - 1][pattern].append(
                        {"System result": instance['System result'], "User result": instance['User result']})
    if os.path.isfile(medium_file):
        data = json.load(open(medium_file, 'r'))
        for pattern in data:
            if pattern == 'overall':
                continue
            medium['tp'].append({pattern: []})
            medium['fn'].append({pattern: []})
            medium['fp'].append({pattern: []})
            for instance in data[pattern]:
                if instance['tp'] > 0:
                    medium['tp'][len(medium['tp'])-1][pattern].append(
                        {"System result": instance['System result'], "User result": instance['User result']})
                if instance['fn'] > 0:
                    medium['fn'][len(medium['fn']) - 1][pattern].append(
                        {"System result": instance['System result'], "User result": instance['User result']})
                if instance['fp'] > 0:
                    medium['fp'][len(medium['fp']) - 1][pattern].append(
                        {"System result": instance['System result'], "User result": instance['User result']})
    if os.path.isfile(hard_file):
        data = json.load(open(hard_file, 'r'))
        for pattern in data:
            if pattern == 'overall':
                continue
            hard['tp'].append({pattern: []})
            hard['fn'].append({pattern: []})
            hard['fp'].append({pattern: []})
            for instance in data[pattern]:
                if instance['tp'] > 0:
                    hard['tp'][len(hard['tp'])-1][pattern].append(
                        {"System result": instance['System result'], "User result": instance['User result']})
                if instance['fn'] > 0:
                    hard['fn'][len(hard['fn']) - 1][pattern].append(
                        {"System result": instance['System result'], "User result": instance['User result']})
                if instance['fp'] > 0:
                    hard['fp'][len(hard['fp']) - 1][pattern].append(
                        {"System result": instance['System result'], "User result": instance['User result']})
        return {'simple': simple, 'medium': medium, 'hard': hard}


@login_required()
def dashboard(request):
    if request.GET.get('errors-field'):
        error = {request.GET.get('errors-field'): request.GET.get('errors_text')}
    else:
        error = None
    posts = DashboardPost.objects.all()
    pattern_form = RequestForm()
    req = Request.objects.filter(user=request.user.id).order_by('-request_date', '-request_id')
    if len(req) == 0:
        req = None
    else:
        req = req[0]
    patterns_list = []
    # 3 types of complexity have different results
    simple = {'tp_list': [], 'tp_fn_list': [], 'patterns_list': [], 'len': 0}
    medium = {'tp_list': [], 'tp_fn_list': [], 'patterns_list': [], 'len': 0}
    hard = {'tp_list': [], 'tp_fn_list': [], 'patterns_list': [], 'len': 0}
    simple_search = {'fn': [], 'tp': [], 'fp': []}
    medium_search = {'fn': [], 'tp': [], 'fp': []}
    hard_search = {'fn': [], 'tp': [], 'fp': []}
    search_data = {'simple': simple_search, 'medium': medium_search, 'hard': hard_search}
    if req:
        if req.request_exe_status == "Done":
            final_file_path = os.path.join("user_" + str(request.user.id), "req_" + str(req.request_id), 'results',
                                           'overall')
            if not os.path.exists(final_file_path):
                proccess_analysis(request, req, final_file_path)

            simple_file = os.path.join(final_file_path, 'simple.json')
            medium_file = os.path.join(final_file_path, 'medium.json')
            hard_file = os.path.join(final_file_path, 'hard.json')

            if os.path.isfile(simple_file):
                with open(simple_file, 'r') as json_reader:
                    simple_data = json.load(json_reader)
                    simple = proccess_chart_data(simple_data)

            if os.path.isfile(medium_file):
                with open(medium_file, 'r') as json_reader:
                    medium_data = json.load(json_reader)
                    medium = proccess_chart_data(medium_data)

            if os.path.isfile(hard_file):
                with open(hard_file, 'r') as json_reader:
                    hard_data = json.load(json_reader)
                    hard = proccess_chart_data(hard_data)

            search_data = proccess_search_data(final_file_path)

        simple['len'] = len(simple['patterns_list'])
        medium['len'] = len(medium['patterns_list'])
        hard['len'] = len(hard['patterns_list'])
        req_chart_data = {'simple': simple, "medium": medium, "hard": hard}


        return render(request, 'sqlab/dashboard.html',
                      {'posts': posts, 'errors': error, 'req_form': pattern_form, 'req': req,
                       'chart_data': req_chart_data,
                       'search_data': search_data})


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
            for patt in form.cleaned_data.get('pattern_select'):
                reqPat = RequestSelectPattern()
                reqPat.request_id = req.request_id
                reqPat.system_pattern_id = patt.pattern_id
                reqPat.save()
            return HttpResponseRedirect('/dashboard/')

    return HttpResponseRedirect('/dashboard/')
