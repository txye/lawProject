# -*- coding: utf-8 -*-
'''
id:问题-》答案判断 
info:流程中问题
infos:
'''

import json

def analyze(tree, p, response):
    if p['id'] == 1:
        if tree['info'] == "kt01":
            if "否" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if p['id'] == 2:
        if tree['info'] == "kt02":
            if "否" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if p['id'] == 3:
        if tree['info'] == "kt03":
            if "否" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if p['id'] == 11:
        if tree['info'] == "kt11":
            if "是" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if (p['id'] == 121 and tree['info'] == "kt121") or \
        (p['id'] == 122 and tree['info'] == "kt122") or \
        (p['id'] == 123 and tree['info'] == "kt123") or \
        (p['id'] == 124 and tree['info'] == "kt124"):
            if "否" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if p['id'] == 21:
        if tree['info'] == "kt121":
            if "否" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if p['id'] == 32:
        if tree['info'] == "kt32":
            if "否" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if (p['id'] == 41 and tree['info'] == "kt41") or \
        (p['id'] == 42 and tree['info'] == "kt42"):
            if "否" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if (p['id'] == 51 and tree['info'] == "kt51") or \
        (p['id'] == 52 and tree['info'] == "kt52"):
            if "否" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if (p['id'] == 61 and tree['info'] == "kt61") or \
        (p['id'] == 62 and tree['info'] == "kt62") or \
        (p['id'] == 63 and tree['info'] == "kt63") or \
        (p['id'] == 64 and tree['info'] == "kt64") or \
        (p['id'] == 65 and tree['info'] == "kt65"):
            if "否" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if p['id'] == 71:
        if tree['info'] == "kt71":
            if "否" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if p['id'] == 81:
        if tree['info'] == "kt81":
            if "否" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    if (p['id'] == 91 and tree['info'] == "kt91") or \
        (p['id'] == 92 and tree['info'] == "kt92") or \
        (p['id'] == 93 and tree['info'] == "kt93"):
            if "否" in response:
                tree['result'] = False
            else:
                tree['result'] = True
    return 'result' in tree

def ask(tree, problems):
    info_id = tree['info']
    
    for p in problems:
        if info_id in p['infos']:
            print p['question']
            response = raw_input()
            response = response.decode('gbk').encode('utf8')
            if info_id == "kt00":
                return response	
            if analyze(tree, p, response):
                break

    if 'result' not in tree:
        tree['result'] = False
        print "Not enough questions for info:"
        print tree

def judge(tree, problems):
    if 'info' in tree:
        if tree['info'] == "kt00":
            branchKey = ask(tree, problems)
            for branch in tree['conditions']:
                if branchKey in branch['name'].encode('utf8'):
                    break
            tree['result'] = judge(branch, problems)
        else:
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
        #print "你犯了盗窃罪"
        print "YES"
    else:
        #print "你没有犯盗窃罪"
        print "NO"



if __name__ == '__main__':
    process("ds_keti.json", "ps_keti.json")
