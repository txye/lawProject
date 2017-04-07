# -*- coding: utf-8 -*-

import json

def analyze(tree, p, response):
    if p['id'] == 0:
        if tree['info'] == "0":
            if "不" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if p['id'] == 1:
        if tree['info'] == "1":
            if "不是" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if p['id'] == 2:
        if tree['info'] == "2":
            if "不" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if p['id'] == 3:
        if tree['info'] == "3":
            if "没" in response:
                tree['result'] = False
            else:
                tree['result'] = True

    return 'result' in tree

def ask(tree, problems):
    info_id = int(tree['info'])

    for p in problems:
        if info_id in p['infos']:
            print p['question']
            response = raw_input()
            if analyze(tree, p, response):
                break

    if 'result' not in tree:
        tree['result'] = False
        print "Not enough questions for info:"
        print tree

def judge(tree, problems):
    if 'info' in tree:
        if 'result' not in tree:
            ask(tree, problems)
        return tree['result']
    else:
        result = judge(tree['conditions'][0], problems)
        for i in range(len(tree['conditions']))[1:]:
            if tree['logic'] == 'and':
                result = result and judge(tree['conditions'][i], problems)
                if not result:
                    return False;
            else:
                if result:
                    return True
                result = result or judge(tree['conditions'][i], problems)
        return result


def process(data_file, problem_file):
    with open(data_file) as f:
        s = f.read()
    data = json.loads(s)

    with open(problem_file) as f:
        s = f.read()
    problems = json.loads(s)['problem-list']

    tree = data['sin']

    result = judge(tree, problems)

    if result:
        print "你犯了盗窃罪"
    else:
        print "你没有犯盗窃罪"



if __name__ == '__main__':
    process("ds.json", "ps.json")
