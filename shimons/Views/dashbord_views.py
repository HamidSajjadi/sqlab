import datetime, os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from shimons.forms import RequestForm, CompareRequest
from shimons.Views.view_misc import get_chart_data_from_folder, save_file, \
    proccess_analysis, proccess_search_data
from shimons.models import DashboardPost, Request, DetectionAlgorithm, RequestAttachPattern, \
    RequestSelectPattern
from Documentations import Documentation

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

    search_data = {}
    req_chart_data = []
    compare_chart_data = []
    comp_req_id = None
    if req:
        if req.system_exe_status == '100':
            ordinal_file_path = os.path.join("user_" + str(request.user.id), "req_" + str(req.request_id), 'results',
                                             'ordinal',
                                             'overall')
            if not os.path.exists(ordinal_file_path):
                proccess_analysis(req)

            comp_req_id = request.GET.get("request")
            if comp_req_id:
                comp_req = Request.objects.get(request_id=comp_req_id)
                if comp_req and comp_req.system_exe_status == '100':
                    comp_final_path = os.path.join("user_" + str(comp_req.user_id),
                                                   "req_" + str(comp_req.request_id), 'results', 'benchmark',
                                                   'overall')

                    if not os.path.exists(comp_final_path):
                        proccess_analysis(comp_req)

                    compare_chart_data = get_chart_data_from_folder(comp_final_path)
                    # compare_chart_data.update({"req_id": comp_req_id})

            req_chart_data = get_chart_data_from_folder(ordinal_file_path)
            search_data = proccess_search_data(ordinal_file_path)

    return render(request, 'sqlab/dashboard.html',
                  {'posts': posts, 'errors': error, 'req_form': pattern_form, 'req': req,
                   'chart_data': req_chart_data,
                   'documentations': Documentation,
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
