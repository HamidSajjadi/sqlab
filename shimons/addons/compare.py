import os

from shimons.addons.file_reader import read_patterns
import json


def compare_patterns(user_file_path, sys_file_path, resultPath, prefix=None):
    # user_file_path = 'C:\\Users\\S Hamid\\Desktop\\khosravi\\compare\\data\\user_out.json'
    # sys_file_path = 'C:\\Users\\S Hamid\\Desktop\\khosravi\\compare\\data\\sys_out.json'

    # read generated answers
    user_pattern_list = read_patterns(user_file_path)

    # read the correct answers
    sys_pattern_list = read_patterns(sys_file_path)
    result_dict = {}
    overall_tp, overall_fp, overall_fn = 0, 0, 0
    # print('>> PATTERNS IN SYSTEM FILE:')
    for sys_p in sys_pattern_list:
        # print('\nPATTERN: {}'.format(sys_p.name))
        # print('System result: {}'.format(sys_p))

        tp, fp, fn = 0, 0, 0

        # find this pattern in user file
        usr_p = None
        for p in user_pattern_list:
            if p.name == sys_p.name:
                usr_p = p

        if usr_p is None:
            # print('-- There is no such pattern in user file.')
            overall_fn += 1
            fn += len(sys_p.inst_list)
        else:  # system file and user file contain this pattern
            # print('User result: {}'.format(usr_p))
            overall_tp += 1

            # check instances
            for sys_inst in sys_p.inst_list:
                if sys_inst in usr_p.inst_list:
                    tp += 1
                else:
                    fn += 1
            for usr_inst in usr_p.inst_list:
                if usr_inst not in sys_p.inst_list:
                    fp += 1
        # print('TP = {}\nFN = {}\nFP = {}'.format(tp, fn, fp))
        result_dict.update(
            {sys_p.name: {'tp': tp, 'fp': fp, 'fn': fn, 'System result': str(sys_p), 'User result': str(usr_p)}})

    # print('\n\n>> PATTERNS ONLY IN USER FILE:')
    for usr_p in user_pattern_list:
        # find this pattern in system file

        tp, fp, fn = 0, 0, 0

        sys_p = None
        for p in sys_pattern_list:
            if p.name == usr_p.name:
                sys_p = p
        if sys_p is None:
            # print('\nPATTERN: {}'.format(sys_p.name))
            # print(usr_p)
            overall_fp += 1
            fp += len(sys_p.inst_list)
            # print('TP = {}\nFN = {}\nFP = {}'.format(tp, fn, fp))
            result_dict.update({sys_p.name: {'tp': tp, 'fp': fp, 'fn': fn}})

            # if overall_fp == 0:
            # print('-- No pattern!')

    # print('\n================')
    # print('Overall TP = {}'.format(overall_tp))
    # print('Overall FN = {}'.format(overall_fn))
    # print('Overall FP = {}'.format(overall_fp))
    result_dict.update({'overall': {'tp': overall_tp, 'fp': overall_fp, 'fn': overall_fn}})
    if not os.path.exists(resultPath):
        os.makedirs(resultPath)
    if prefix:
        with open(os.path.join(resultPath, prefix + '_data.json'), 'w') as fp:
            json.dump(result_dict, fp)
    else:
        with open(os.path.join(resultPath, 'data.json'), 'w') as fp:
            json.dump(result_dict, fp)


def summarize(file_path_set, output_path, filename):
    pattern_dict = dict()
    tp, fp, fn, tn = 0, 0, 0, 0

    for file_path in file_path_set:
        file = json.load(open(file_path))
        for k, v in file.items():
            if k == 'overall':
                continue

            if k in pattern_dict.keys():
                pattern_dict[k].append(v)
            else:
                pattern_dict[k] = [v]

            tp += v['tp']
            fp += v['fp']
            fn += v['fn']

    acc = (tp + tn) / (tp + fn + fp + tn)
    prc = tp / (tp + fp) if (tp + fp) > 0 else -1
    rec = tp / (tp + fn) if (tp + fn) > 0 else -1
    fsc = 2 * prc * rec / (prc + rec) if (prc + rec) > 0 else -1

    pattern_dict['overall'] = {'tp': tp, 'fp': fp, 'fn': fn, 'acc': acc, 'prc': prc, 'rec': rec, 'fsc': fsc}
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(os.path.join(output_path, filename), 'w') as writer:
        json.dump(pattern_dict, writer, indent=' ')

# summarize({'simple_data.json', 'simple_data (copy).json'}, 'summarize.json')
