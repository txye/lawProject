# -*- coding: utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

"""
Law demo
流程如下：
zt：主体
sf：主观方面
kt：客体
kf：客观方面
zq：违法阻却事由

回答：
肯定回答请使用“是”，否定回答请用“否”
回答盗窃东西时，请回答偷盗的相关物品
"""

def analyze(treeRelation, questionList, response):
    # 主体
    if questionList['id'] == "zt0" and treeRelation['info'] == "zt0":
            if "否" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True
    if questionList['id'] == "zt1" and treeRelation['info'] == "zt1":
            if "否" in response:
                treeRelation['result'] = True
            else:
                treeRelation['result'] = False
    if questionList['id'] == "zt3" and treeRelation['info'] == "zt3":
            if "否" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True

    # 客体
    if questionList['id'] == "kt01" and treeRelation['info'] == "kt01":
            if "否" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True
    if questionList['id'] == "kt02" and treeRelation['info'] == "kt02":
            if "否" in response:
                treeRelation['result'] = True
            else:
                treeRelation['result'] = False
    if questionList['id'] == "kt03" and treeRelation['info'] == "kt03":
            if "否" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True
    if questionList['id'] == "kt11" and treeRelation['info'] == "kt11":
            if "是" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True
    if (questionList['id'] == "kt121" and treeRelation['info'] == "kt121") or \
        (questionList['id'] == "kt122" and treeRelation['info'] == "kt122") or \
        (questionList['id'] == "kt123" and treeRelation['info'] == "kt123") or \
        (questionList['id'] == "kt124" and treeRelation['info'] == "kt124"):
            if "否" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True
    if questionList['id'] == "kt32" and  treeRelation['info'] == "kt32":
            if "否" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True
    if (questionList['id'] == "kt41" and treeRelation['info'] == "kt41") or \
        (questionList['id'] == "kt42" and treeRelation['info'] == "kt42"):
            if "否" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True
    if (questionList['id'] == "kt51" and treeRelation['info'] == "kt51") or \
        (questionList['id'] == "kt52" and treeRelation['info'] == "kt52"):
            if "否" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True
    if (questionList['id'] == "kt61" and treeRelation['info'] == "kt61") or \
        (questionList['id'] == "kt62" and treeRelation['info'] == "kt62") or \
        (questionList['id'] == "kt63" and treeRelation['info'] == "kt63") or \
        (questionList['id'] == "kt64" and treeRelation['info'] == "kt64") or \
        (questionList['id'] == "kt65" and treeRelation['info'] == "kt65"):
            if "否" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True
    if questionList['id'] == "kt71" and treeRelation['info'] == "kt71":
            if "否" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True
    if questionList['id'] == "kt81" and treeRelation['info'] == "kt81":
            if "否" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True
    if (questionList['id'] == "kt91" and treeRelation['info'] == "kt91") or \
        (questionList['id'] == "kt92" and treeRelation['info'] == "kt92") or \
        (questionList['id'] == "kt93" and treeRelation['info'] == "kt93"):
            if "否" in response:
                treeRelation['result'] = False
            else:
                treeRelation['result'] = True
    if questionList['id'] == "ktDefault" and treeRelation['info'] == "ktDefault":
        treeRelation['result'] = True

    # 客观方面
    if questionList['id'] == "kf021" and treeRelation['info'] == "kf021":
        if "否" in response:
            treeRelation['result'] = False
        else:
            treeRelation['result'] = True
    if (questionList['id'] == "kf0220" and treeRelation['info'] == "kf0220") or \
        (questionList['id'] == "kf0221" and treeRelation['info'] == "kf0221") or \
        (questionList['id'] == "kf0222" and treeRelation['info'] == "kf0222") or \
        (questionList['id'] == "kf0223" and treeRelation['info'] == "kf0223") or \
        (questionList['id'] == "kf0224" and treeRelation['info'] == "kf0224") or \
        (questionList['id'] == "kf0225" and treeRelation['info'] == "kf0225") or \
        (questionList['id'] == "kf0226" and treeRelation['info'] == "kf0226") or \
        (questionList['id'] == "kf0227" and treeRelation['info'] == "kf0227") or \
        (questionList['id'] == "kf0228" and treeRelation['info'] == "kf0228"):
        if "否" in response:
            treeRelation['result'] = False
        else:
            treeRelation['result'] = True
    if questionList['id'] == "kf023" and treeRelation['info'] == "kf023":
        if "否" in response:
            treeRelation['result'] = False
        else:
            treeRelation['result'] = True
    if questionList['id'] == "kf111" and treeRelation['info'] == "kf111":
        if "否" in response:
            treeRelation['result'] = False
        else:
            treeRelation['result'] = True
    if questionList['id'] == "kf112" and treeRelation['info'] == "kf112":
        if "否" in response:
            treeRelation['result'] = False
        else:
            treeRelation['result'] = True
    if (questionList['id'] == "kf11311" and treeRelation['info'] == "kf11311") or \
        (questionList['id'] == "kf11312" and treeRelation['info'] == "kf11312") or \
        (questionList['id'] == "kf11313" and treeRelation['info'] == "kf11313") or \
        (questionList['id'] == "kf1132" and treeRelation['info'] == "kf1132"):
        if "否" in response:
            treeRelation['result'] = False
        else:
            treeRelation['result'] = True
    if questionList['id'] == "kf114" and treeRelation['info'] == "kf114":
        if "否" in response:
            treeRelation['result'] = False
        else:
            treeRelation['result'] = True

     # 主观方面
    if (questionList['id'] == "sf1" and treeRelation['info'] == "sf1") or \
        (questionList['id'] == "sf2" and treeRelation['info'] == "sf2"):
        if "否" in response:
            treeRelation['result'] = False
        else:
            treeRelation['result'] = True

    # 不具备违法阻却事由
    if (questionList['id'] == "zq1" and treeRelation['info'] == "zq1") or \
        (questionList['id'] == "zq2" and treeRelation['info'] == "zq2"):
        if "否" in response:
            treeRelation['result'] = True
        else:
            treeRelation['result'] = False
    return 'result' in treeRelation

def ask(treeRelation, problems):
    info_id = treeRelation['info']
    
    for questionList in problems:
        if info_id in questionList['infos']:
            if "Default" not in info_id:
                print questionList['question']
                response = raw_input()
                response = response.decode('gbk').encode('utf8')
            else:
                response = ""
            if info_id == "kt00":
                return response
            if analyze(treeRelation, questionList, response):
                break

    if 'result' not in treeRelation:
        treeRelation['result'] = False
        print "Not enough questions for info:"
        print treeRelation

def judge(treeRelation, problems):
    if 'info' in treeRelation:
        if treeRelation['info'] == "kt00":
            branchKey = ask(treeRelation, problems)
            for branch in treeRelation['conditions']:
                if branchKey in branch['name'].encode('utf8'):
                    break
            treeRelation['result'] = judge(branch, problems)
        else:
            if 'result' not in treeRelation:
                ask(treeRelation, problems)
        return treeRelation['result']
    else:
        result = judge(treeRelation['conditions'][0], problems)
        for i in range(len(treeRelation['conditions']))[1:]:
            if treeRelation['logic'] == 'and':
                result = result and judge(treeRelation['conditions'][i], problems)
                if not result:
                    return False;
            else:
                if result:
                    return True
                result = result or judge(treeRelation['conditions'][i], problems)
        return result


def process(data_file, problem_file):
    with open(data_file) as file:
        text = file.read()
    data = json.loads(text)
    with open(problem_file) as file:
        text = file.read()
    problems = json.loads(text)['problem-list']
    treeRelation = data['sin']
    resultConcluded = judge(treeRelation, problems)
    if resultConcluded:
        #print "你犯了盗窃罪"
        print "YES"
    else:
        #print "你没有犯盗窃罪"
        print "NO"


if __name__ == '__main__':
    process("ds.json", "ps.json")

