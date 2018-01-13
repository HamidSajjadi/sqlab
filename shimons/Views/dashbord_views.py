import datetime
import os
import json
from django.shortcuts import render
from shimons.models import DashboardPost, Request, DetectionAlgorithm, RequestAttachPattern, AnalysisResult, TagetCode, \
    TargetCodeConfig, RequestSelectPattern
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from shimons.forms import RequestForm, CompareRequest
from shimons.addons import compare


def save_file(file, path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def proccess_analysis(req, final_file_path):
    analysis = AnalysisResult.objects.filter(request=req.request_id)
    file_set = {'simple': [], 'medium': [], 'hard': []}
    for anal in analysis:  #:D
        targetCode = TagetCode.objects.get(targetcode_id=anal.targetcode_id)
        complexity = TargetCodeConfig.objects.get(complexity_id=targetCode.complexity_id)
        result_path = os.path.join("user_" + str(req.user_id), "req_" + str(req.request_id),
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
                    simple['tp'][len(simple['tp']) - 1][pattern].append(
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
                    medium['tp'][len(medium['tp']) - 1][pattern].append(
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
                    hard['tp'][len(hard['tp']) - 1][pattern].append(
                        {"System result": instance['System result'], "User result": instance['User result']})
                if instance['fn'] > 0:
                    hard['fn'][len(hard['fn']) - 1][pattern].append(
                        {"System result": instance['System result'], "User result": instance['User result']})
                if instance['fp'] > 0:
                    hard['fp'][len(hard['fp']) - 1][pattern].append(
                        {"System result": instance['System result'], "User result": instance['User result']})
        return {'simple': simple, 'medium': medium, 'hard': hard}


def get_chart_data_from_folder(final_file_path):
    simple = {'tp_list': [], 'tp_fn_list': [], 'patterns_list': [], 'len': 0}
    medium = {'tp_list': [], 'tp_fn_list': [], 'patterns_list': [], 'len': 0}
    hard = {'tp_list': [], 'tp_fn_list': [], 'patterns_list': [], 'len': 0}
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

    simple['len'] = len(simple['patterns_list'])
    medium['len'] = len(medium['patterns_list'])
    hard['len'] = len(hard['patterns_list'])
    return {'simple': simple, "medium": medium, "hard": hard}


@login_required()
def dashboard(request):
    if request.GET.get('errors-field'):
        error = {request.GET.get('errors-field'): request.GET.get('errors_text')}
    else:
        error = None
    posts = DashboardPost.objects.all()
    pattern_form = RequestForm()
    compare_form = CompareRequest()
    compare_form.fields["request"].queryset = Request.objects.filter(system_exe_status='100')
    req = Request.objects.filter(user=request.user.id).order_by('-request_date', '-request_id')
    if len(req) == 0:
        req = None
    else:
        req = req[0]
    # 3 types of complexity have different results

    simple_search = {'fn': [], 'tp': [], 'fp': []}
    medium_search = {'fn': [], 'tp': [], 'fp': []}
    hard_search = {'fn': [], 'tp': [], 'fp': []}
    search_data = {'simple': simple_search, 'medium': medium_search, 'hard': hard_search}
    req_chart_data = []
    compare_chart_data = []
    comp_req_id = None
    if req:
        if req.system_exe_status == '100':

            final_file_path = os.path.join("user_" + str(request.user.id), "req_" + str(req.request_id), 'results',
                                           'overall')
            if not os.path.exists(final_file_path):
                proccess_analysis(req, final_file_path)

            comp_req_id = request.GET.get("request")
            if comp_req_id:
                comp_req = Request.objects.get(request_id=comp_req_id)
                if comp_req and comp_req.system_exe_status == '100':
                    comp_final_path = os.path.join("user_" + str(comp_req.user_id),
                                                   "req_" + str(comp_req.request_id), 'results',
                                                   'overall')

                    if not os.path.exists(comp_final_path):
                        proccess_analysis(comp_req, comp_final_path)

                    compare_chart_data = get_chart_data_from_folder(comp_final_path)
                    # compare_chart_data.update({"req_id": comp_req_id})

            req_chart_data = get_chart_data_from_folder(final_file_path)
            search_data = proccess_search_data(final_file_path)
        print('req,', req_chart_data)
        print('comp', compare_chart_data)
        return render(request, 'sqlab/dashboard.html',
                      {'posts': posts, 'errors': error, 'req_form': pattern_form, 'req': req,
                       'chart_data': req_chart_data,
                       'search_data': search_data,
                       'compare_form': compare_form,
                       'compare_chart_data': compare_chart_data,
                       'compare_req_id': comp_req_id})


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


@login_required()
def download_result(request, level, req_id):
    req = Request.objects.get(request_id=req_id)
    print(req.request_id, req.user_id)
    if req is None:
        return HttpResponse("Request id wrong")
    if req.user_id != request.user.id:
        return HttpResponse("You are not authorized to access this file")
    if req.system_exe_status != '100':
        return HttpResponse("Your request has not yet been proccesed")

    final_file_path = os.path.join("user_" + str(request.user.id), "req_" + str(req.request_id), 'results',
                                   'overall')
    final_file = os.path.join("user_" + str(request.user.id), "req_" + str(req.request_id), 'results',
                              'overall', level + '.json')

    if not os.path.isfile(final_file):
        proccess_analysis(req, final_file_path)
        if not os.path.isfile(final_file):
            return HttpResponse("This request has no result for {} level".format(level))

    tf = open(final_file, 'r')
    return HttpResponse(tf, content_type='application/json')
