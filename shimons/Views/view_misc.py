import os, json
from shimons.addons import compare
from shimons.models import DashboardPost, Request, DetectionAlgorithm, RequestAttachPattern, AnalysisResult, TagetCode, \
    TargetCodeConfig, RequestSelectPattern, FinalResult


def proccess_analysis(req):
    ordinal_file_path = os.path.join("user_" + str(req.user_id), "req_" + str(req.request_id), 'results',
                                     'ordinal',
                                     'overall')
    benchmark_file_path = os.path.join("user_" + str(req.user_id), "req_" + str(req.request_id), 'results',
                                       'benchmark',
                                       'overall')
    analysis = AnalysisResult.objects.filter(request=req.request_id)
    ordinal_file_set = {}
    benchmark_file_set = {}
    for anal in analysis:  #:D
        targetCode = TagetCode.objects.get(targetcode_id=anal.targetcode_id)
        complexity = TargetCodeConfig.objects.get(config_id=targetCode.config_id)
        ordinal_result_path = os.path.join("user_" + str(req.user_id), "req_" + str(req.request_id),
                                           'results', "ordinal",
                                           'analysis_' + str(anal.request_id) + '_' + str(anal.targetcode_id),
                                           )
        benchmark_result_path = os.path.join("user_" + str(req.user_id), "req_" + str(req.request_id),
                                             'results', "benchmark",
                                             'analysis_' + str(anal.request_id) + '_' + str(anal.targetcode_id),
                                             )
        if complexity.category == "ORDINAL":
            compare.compare_patterns(anal.detectionresult_path, targetCode.patternsinfo_path, ordinal_result_path,
                                     prefix=complexity.complexity_level)
            anal.analysisresult_path = os.path.join(ordinal_result_path, complexity.complexity_level + '_data.json')
            if complexity.complexity_level in ordinal_file_set:
                ordinal_file_set[complexity.complexity_level].append(anal.analysisresult_path)
            else:
                ordinal_file_set.update({complexity.complexity_level: [anal.analysisresult_path]})
        elif complexity.category == "BENCHMARK":
            compare.compare_patterns(anal.detectionresult_path, targetCode.patternsinfo_path, benchmark_result_path,
                                     prefix=complexity.complexity_level)
            anal.analysisresult_path = os.path.join(benchmark_result_path, complexity.complexity_level + '_data.json')
            if complexity.complexity_level in benchmark_file_set:
                benchmark_file_set[complexity.complexity_level].append(anal.analysisresult_path)
            else:
                benchmark_file_set.update({complexity.complexity_level: [anal.analysisresult_path]})

        anal.save()

    for level in benchmark_file_set:
        compare.summarize(benchmark_file_set[level], benchmark_file_path, level + '.json')
    for level in ordinal_file_set:
        compare.summarize(ordinal_file_set[level], ordinal_file_path, level + '.json')
    get_result(req)


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
    return_data = {}
    for file in os.listdir(final_file_path):
        if file.endswith(".json"):
            return_data.update({file.split('.')[0]: {'fn': [], 'tp': [], 'fp': []}})
            temp = {'fn': [], 'tp': [], 'fp': []}
            data = json.load(open(os.path.join(final_file_path, file), 'r'))
            for pattern in data:
                if pattern == 'overall':
                    continue
                temp['tp'].append({pattern: []})
                temp['fn'].append({pattern: []})
                temp['fp'].append({pattern: []})
                for instance in data[pattern]:
                    if instance['tp'] > 0:
                        temp['tp'][len(temp['tp']) - 1][pattern].append(
                            {"System result": instance['System result'], "User result": instance['User result']})
                    if instance['fn'] > 0:
                        temp['fn'][len(temp['fn']) - 1][pattern].append(
                            {"System result": instance['System result'], "User result": instance['User result']})
                    if instance['fp'] > 0:
                        temp['fp'][len(temp['fp']) - 1][pattern].append(
                            {"System result": instance['System result'], "User result": instance['User result']})
                        # simple = {'fn': [], 'tp': [], 'fp': []}
                        # medium = {'fn': [], 'tp': [], 'fp': []}
                        # hard = {'fn': [], 'tp': [], 'fp': []}

                        # simple_file = os.path.join(final_file_path, 'simple.json')
                        # medium_file = os.path.join(final_file_path, 'medium.json')
                        # hard_file = os.path.join(final_file_path, 'hard.json')
                        # if os.path.isfile(simple_file):
                        #     data = json.load(open(simple_file, 'r'))
                        #     for pattern in data:
                        #         if pattern == 'overall':
                        #             continue
                        #         simple['tp'].append({pattern: []})
                        #         simple['fn'].append({pattern: []})
                        #         simple['fp'].append({pattern: []})
                        #         for instance in data[pattern]:
                        #             if instance['tp'] > 0:
                        #                 simple['tp'][len(simple['tp']) - 1][pattern].append(
                        #                     {"System result": instance['System result'], "User result": instance['User result']})
                        #             if instance['fn'] > 0:
                        #                 simple['fn'][len(simple['fn']) - 1][pattern].append(
                        #                     {"System result": instance['System result'], "User result": instance['User result']})
                        #             if instance['fp'] > 0:
                        #                 simple['fp'][len(simple['fp']) - 1][pattern].append(
                        #                     {"System result": instance['System result'], "User result": instance['User result']})
                        # if os.path.isfile(medium_file):
                        #     data = json.load(open(medium_file, 'r'))
                        #     for pattern in data:
                        #         if pattern == 'overall':
                        #             continue
                        #         medium['tp'].append({pattern: []})
                        #         medium['fn'].append({pattern: []})
                        #         medium['fp'].append({pattern: []})
                        #         for instance in data[pattern]:
                        #             if instance['tp'] > 0:
                        #                 medium['tp'][len(medium['tp']) - 1][pattern].append(
                        #                     {"System result": instance['System result'], "User result": instance['User result']})
                        #             if instance['fn'] > 0:
                        #                 medium['fn'][len(medium['fn']) - 1][pattern].append(
                        #                     {"System result": instance['System result'], "User result": instance['User result']})
                        #             if instance['fp'] > 0:
                        #                 medium['fp'][len(medium['fp']) - 1][pattern].append(
                        #                     {"System result": instance['System result'], "User result": instance['User result']})
                        # if os.path.isfile(hard_file):
                        #     data = json.load(open(hard_file, 'r'))
                        #     for pattern in data:
                        #         if pattern == 'overall':
                        #             continue
                        #         hard['tp'].append({pattern: []})
                        #         hard['fn'].append({pattern: []})
                        #         hard['fp'].append({pattern: []})
                        #         for instance in data[pattern]:
                        #             if instance['tp'] > 0:
                        #                 hard['tp'][len(hard['tp']) - 1][pattern].append(
                        #                     {"System result": instance['System result'], "User result": instance['User result']})
                        #             if instance['fn'] > 0:
                        #                 hard['fn'][len(hard['fn']) - 1][pattern].append(
                        #                     {"System result": instance['System result'], "User result": instance['User result']})
                        #             if instance['fp'] > 0:
                        #                 hard['fp'][len(hard['fp']) - 1][pattern].append(
                        #                     {"System result": instance['System result'], "User result": instance['User result']})
                        #     return {'simple': simple, 'medium': medium, 'hard': hard}

            return_data.update({file.split('.')[0]: temp})
    return return_data


def get_chart_data_from_folder(final_file_path):
    return_data = {}
    for file in os.listdir(final_file_path):
        if file.endswith(".json"):
            with open(os.path.join(final_file_path, file), 'r') as json_reader:
                data = json.load(json_reader)
                temp = proccess_chart_data(data)
                temp['len'] = len(temp)
                return_data.update({os.path.splitext(file)[0]: temp})
    return return_data


def save_final_result(req, category):
    file_path = os.path.join("user_" + str(req.user_id), "req_" + str(req.request_id), 'results',
                             category.lower(),
                             'overall')
    data = get_chart_data_from_folder(file_path)
    tp_list = []
    fn_list = []
    fp_list = []
    fsc_list = []
    for key in data:
        tp_list.append(data[key]['overall']['tp'])
        fn_list.append(data[key]['overall']['fn'])
        fp_list.append(data[key]['overall']['fp'])
        fsc_list.append(data[key]['overall']['fsc'])
    final_res = FinalResult()
    final_res.request = req
    final_res.category = category
    final_res.execution_times = AnalysisResult.objects.filter(request=req,
                                                              targetcode__config__category=category).count()
    final_res.tp_avg = sum(tp_list) / len(tp_list)
    final_res.fn_avg = sum(fn_list) / len(fn_list)
    final_res.fp_avg = sum(fp_list) / len(fp_list)
    final_res.tn_avg = 0
    final_res.fm_avg = sum(fsc_list) / len(fsc_list)
    final_res.rank = 100
    final_res.save()


def get_result(req):
    result = FinalResult.objects.filter(request=req)
    if result.count() == 0:
        save_final_result(req, "BENCHMARK")
        save_final_result(req, "ORDINAL")


def save_file(file, path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
