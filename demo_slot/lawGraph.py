#encoding: utf-8
import datetime
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Element(object):
    def __init__(self, elemId, elemName, elemPrio):
        self.elemId = elemId
        self.elemName = elemName
        self.elemPrio = elemPrio

def read_factor(nameElemDict, idNameDict):
    file = open("factor.ttl")
    mapNum = 1;
    while 1:
        line = file.readline()
        if not line:
            break
        match = re.match(ur'<(\S+)>', line)
        if match:
            elemId = match.group(1)
            continue
        match = re.match(ur'\s+Law:要件名\s+\"(\S+)\".*', line.decode('utf8'))
        if match:
            elemName =str(match.group(1))
            continue
        match = re.match(ur'\s+Law:要件级别\s+\"(\d+)\".*', line.decode('utf8'))
        if match:
            elemPrio =match.group(1)
            Elem = Element(elemId, elemName, elemPrio)
            nameElemDict[elemName] = Elem
            idNameDict[elemId] =elemName
            if not idNumberDict.has_key(elemName):
                idNumberDict[elemName] = mapNum
                mapNum += 1

def read_slot(subObjList, subObjSlot, subobjflag):
    """
    解析原子规则中的槽信息
    """
    for item in subObjList:
        hyphenNum = item.count('-')
        if hyphenNum > 2:
            if subobjflag == 'object':
                match = re.match(ur'.*-(\S+)-\S+-(\S+)$', item)
            elif subobjflag == 'subject':
                match = re.match(ur'.*-\S+-(\S+)-(\S+)$', item)
        elif hyphenNum == 2:
            if subobjflag == 'object':
                match = re.match(ur'.*-(\S+)-(\S+)$', item)
            elif subobjflag == 'subject':
                match = re.match(ur'.*-\S+-(\S+)$', item)
        elif hyphenNum == 1:
            match = re.match(ur'.*<\S+-(\S+)$', item)
        else:
            match = ""
        if match:
            if not subObjSlot.has_key(match.group(1)):
                subObjSlot[match.group(1)] = set()
            if hyphenNum > 1:
                if len(match.groups()) > 1:
                   value = match.group(2)
                else:
                    value = ""
                subObjSlot[match.group(1)].add(value)
                if(len(subObjList) == 1):
                    return match.group(1), value
            else:
                return match.group(1), ""

def read_rule(idNameDict, lawGraphDict, reverseGraphDict):
    file = open("rule.ttl")
    while 1:
        line = file.readline()
        if not line:
            break
        if re.match(r'@.*', line):
            continue
        match = re.match(ur'\s+Law:\W+\s+\"(OR|AND)\".*', line)
        if match:
            logicRelation =match.group(1)
            listName = []
            listName.append(logicRelation)
            continue
        match = re.match(ur'\s+Law:前提\s+<(\S+)>.*', line.decode('utf8'))
        if match:
            elemId =match.group(1)
            listName.append(idNameDict[elemId])
            continue
        match = re.match(ur'\s+Law:前提\s+"([^a-z]+)".*', line.decode('utf8'))
        if match:
            atomicRule = match.group(1)
            listName.append(atomicRule)
            listSO = atomicRule.split('\t')
            subList = listSO[1].split('>')
            read_slot(subList, subSlot, 'subject')
            objList = listSO[0].split('>')
            read_slot(objList, objSlot, 'object')
            continue
        match = re.match(ur'\s+Law:结论\s+<(\S+)>.*', line.decode('utf8'))
        if match:
            concludeId = match.group(1)
            lawGraphDict[idNameDict[concludeId]] = listName
            if len(listName) > 1:
                for i in range(len(listName))[1:]:
                    reverseGraphDict[listName[i]] = idNameDict[concludeId]      #逆向关系图

"""
1）映射：
    偷|偷盗-》窃取

"""
def match_pattern(inquiryStr, stateSlot):
    """
    获取用户话语中的关键信息，未完成
    目前支持：
        1）提取金额
        2）获取年龄
    例子：
        1）u"盗窃1000元钱也构成犯罪吗"
        2）u"我偷钱的时候是十七周岁，还不满十八周岁，是不是不算犯罪？"
    """
    #inquiryStr = u"我偷钱的时候是十七周岁，还不满十八周岁，是不是不算犯罪？"
    match = re.match(ur'.*[偷 盗窃](.*)元.*', inquiryStr)
    if match:
        amount = int(match.group(1))
        if(amount >= 1000 and amount < 30000):
            money = u"数额较大"
        elif amount >= 30000:
            money = u"数额巨大"
        elif(amount >= 500 and amount < 15000):
            money = u"数额较大标准的50%"
        else:
            money = u"数额不满足"
        stateSlot[u"对象"].add(money)

    match = re.match(ur'.*[满 是](.*?)周?岁.*', inquiryStr)
    if match:
        age = match.group(1)
        stateSlot[u"年龄"] = age




def compute_age(factorDate, stateSlot):
    factorTime = [int(item) for item in factorDate.split('-' )]
    for birthDay in stateSlot[u'出生日期']:
        birthTime = [int(item) for item in birthDay.split('-')]
    yearDelta = factorTime[0] - birthTime[0]
    if factorTime[1] <= birthTime[1]:
        if factorTime[2] < birthTime[2]:
            yearDelta -= 1
    print yearDelta

def fill_slot(inquiryStr, stateSlot):
    match_pattern(inquiryStr, stateSlot)
    for key, value in objSlot.items():
        objList = value
        for item in objList:
            if not wordMap.has_key(item):
                wordMap[item] = [item]
            for elem in wordMap[item]:      #映射后填槽
                if elem in inquiryStr:
                    stateSlot[key].add(item)

def solve_answer(answerType):
    response = raw_input()
    #response = response.decode('gbk').encode('utf8')
    if answerType == 'yes_or_not':
        if response == '是':
            return True
        else:
            return False
    elif answerType == 'condition':
        if isStatisfyState in response:
            return True
        else:
            return False
    elif answerType == 'information':
        return response

def ask_user(questionSet, isStatisfyState):
    for ques in questionSet:
        if ques['name'] == isStatisfyState:
            print ques['question']

def query_slot(slotState, isStatisfyState):
    """
    客观条件和主观条件的所有状态询问，未完成
    目前有两种询问方法：
        1）是否
        2）条件询问（如对"地点"的询问）
    """
    if slotState == u"角色" :
        return True
    elif slotState == u"出生日期":
        if stateSlot[u'年龄']:
            return True
        print u"行为人的出生日期？\n"
        stateSlot["出生日期"] = solve_answer('information')
        return True
    elif slotState == u'主体责任能力':
        ask_user(questionSet, isStatisfyState)
    elif slotState == u'主观方面':
        pass
    elif slotState == u"事件阶段":
        if isStatisfyState == u'案发后':
            print u"请问事件阶段是否已经在案发后？\n"
        return solve_answer('yes_or_not')
    elif slotState == u"后果":
        for item in objSlot:
            if item == isStatisfyState:
                print u"请问您是否导致" + item
            return solve_answer('yes_or_not')
    elif slotState == u"地点":
        print u"请问您当时所在的场所？"
        return solve_answer('yes_or_not')
    elif slotState == u"完成形态":
        if isStatisfyState == u'既遂':
            if len(stateSlot[u"完成形态"]) > 0 and stateSlot[u"完成形态"] != u'既遂':
                return False
            print u"请问您盗窃的物品是否脱离了被害人的控制？\n"
            if solve_answer('yes_or_not'):
                stateSlot[u"完成形态"].add(u"既遂")
                return True
            #五种完成形态需要一一判断
            else:
                stateSlot[u"完成形态"].add(u"非既遂")
                return False
    elif slotState == u'对象':
        pass
    elif slotState == u'时间':
        if stateSlot[u'年龄']:
            age = stateSlot[u'年龄']
        else:
            print u"这件事情发生的时间？\n"
            factorDate = solve_answer('information')
            age = compute_age(factorDate, stateSlot)
        if(int(age) >= 16):
            return True

    elif slotState == u'特殊情况':
        pass
    elif slotState == u'行为':
        pass

def check_states_slot(atomicRule, stateSlot):
    subobjList = atomicRule.split('\t')
    #主体
    subList = subobjList[1].split('>')
    for item in subList:
        if item == "" or item.count('-') < 1:
            continue
        slotState, isStatisfyState = read_slot([item], subSlot, 'subject')
        slotSatisfied = False
        for slot in stateSlot[slotState]:
            if(slot in isStatisfyState):
                result = True
                slotSatisfied = True
                break
        if not slotSatisfied:       #槽为空，引导用户提出问题
            result = query_slot(slotState, isStatisfyState)

    #事件
    objList = [subobjList[0]]
    if subobjList[0].count('[') > 0:
        objList = subobjList[0].split('&')
    if subobjList[0].count('}') > 0:
        objList = subobjList[0].split('}')
    result = False
    for item in objList:
        if not item:
            continue
        atomicList = item.split('>')
        for elem in atomicList:
            if elem == "" or elem.count('-') < 1:
                continue
            slotState, isStatisfyState = read_slot([elem], objSlot, 'object')
            if isStatisfyState == "":
                continue
            if isStatisfyState == u'数额':        #对数额条件的特殊判断，需要参考上文
                 isStatisfyState = reverseGraphDict[atomicRule].decode("utf8")
            slotSatisfied = False
            for slot in stateSlot[slotState]:
                if(slot in isStatisfyState):
                    result = True
                    slotSatisfied = True
                    break
            if not slotSatisfied:       #槽为空，引导用户提出问题
                result = query_slot(slotState, isStatisfyState)
            if item.count('[') > 0:     #或关系
                if result:
                    break
            else:                       #与关系
                if not result:
                    break
        if not result:
            break
    return result

def InitSlot():
    for key in subSlot:
        stateSlot[key] = set()
    stateSlot[u'年龄'] = ""
    for key in objSlot:
        stateSlot[key] = set()

def InitProcess(processSlot, lawGraphDict):
    #processSlot = {"主体":-1, "主观方面":-1, "客体及客观方面":-1, "排除犯罪事由":-1}
    for item in lawGraphDict["盗窃罪"]:
        processSlot[item] = False

def read_problems(problem_file):
    with open(problem_file) as file:
        content = file.read()
    return json.loads(content)['problem-list']

def Init():
    read_factor(nameElemDict, idNameDict)
    read_rule(idNameDict, lawGraphDict, reverseGraphDict)
    questionSet = read_problems("problem.json")
    InitSlot()
    InitProcess(processSlot, lawGraphDict)

def dialog_judge(lawGraphDict, currentNode):
    """
    对话判断主流程
    """
    if not idNumberDict.has_key(currentNode):
        #print currentNode
        return check_states_slot(currentNode,stateSlot)
    else:
        result = dialog_judge(lawGraphDict, lawGraphDict[currentNode][1])
        for i in range(len(lawGraphDict[currentNode]))[2:]:
            conditionNode = lawGraphDict[currentNode][i]
            if lawGraphDict[currentNode][0] == 'AND':
                result = result and dialog_judge(lawGraphDict, conditionNode)
                if not result:
                    return False
            else:
                result = result or dialog_judge(lawGraphDict, conditionNode)
                if result:
                    return True
        return result

def process_run():
    """
    优化方法：
        1）可以先提出几个通用问题，以减少规则匹配
    """
    print u"您好，请问有什么需要帮助的吗？\n"
    #response = solve_answer('information')
    #response = u"偷1000元钱也构成犯罪吗？"
    fill_slot(response, stateSlot)
    if u"窃取" in stateSlot[u"行为"]:
        print u"还偷了其他物品吗\n"     #通用问题一
    response = u"还有信用卡"
    fill_slot(response, stateSlot)
    if stateSlot[u"年龄"] and int(stateSlot[u"年龄"]) >= 16 and int(stateSlot[u"年龄"]) < 18:
        result = dialog_judge(lawGraphDict, "排除犯罪事由")
        processSlot["排除犯罪事由"] = True
    elif u"窃取" in stateSlot[u"行为"]:
        result = dialog_judge(lawGraphDict, "客体及客观方面")
        processSlot["客体及客观方面"] = True
    else:
        result = True

    for key, value in processSlot.items():
        if value:
            continue
        result = result and (lawGraphDict, key)
        if not result:
            break

    if result:
        #print "你犯了盗窃罪"
        print "YES"
    else:
        #print "你没有犯盗窃罪"
        print "NO"

if __name__ == '__main__':
    nameElemDict = {}
    idNameDict = {}     #id到name的映射
    idNumberDict = {}       #id到要件序号的映射
    lawGraphDict = {}
    reverseGraphDict = {}       #关系逆向图
    subSlot = {}        #主观槽
    objSlot = {}        #客观槽
    stateSlot = {}      #状态槽
    processSlot = {}
    wordMap = {u"窃取":[u"偷"]}        #关键词映射图

    Init()
    process_run()

    """
    添加“还有什么需要补充的吗？，承接其他罪名判断”
    """
