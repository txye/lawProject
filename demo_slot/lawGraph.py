#encoding: utf-
# -*- coding: utf-8 -*-
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
    file.close()

def read_slot(subObjList, subObjSlot):
    """
    解析原子规则中的槽信息
    """
    for item in subObjList:
        hyphenNum = item.count('-')
        if hyphenNum > 2:
            match = re.match(ur'.*-(\S+)-\S+-(\S+)$', item)
        elif hyphenNum == 2:
            match = re.match(ur'.*-(\S+)-(\S+)$', item)
        elif hyphenNum == 1:
            match = re.match(ur'.*<\S+-(\S+)$', item)
        else:
            match = ""
        if match:
            if not subObjSlot.has_key(match.group(1)):
                subObjSlot[match.group(1)] = set()
            if hyphenNum > 1:
                subObjSlot[match.group(1)].add(match.group(2))
                if(len(subObjList) == 1):
                    return match.group(1), match.group(2)
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
            read_slot(subList, subSlot)
            objList = listSO[0].split('>')
            read_slot(objList, objSlot)
            continue
        match = re.match(ur'\s+Law:结论\s+<(\S+)>.*', line.decode('utf8'))
        if match:
            concludeId = match.group(1)
            lawGraphDict[idNameDict[concludeId]] = listName
            if len(listName) > 1:
                for i in range(len(listName))[1:]:
                    reverseGraphDict[listName[i]] = idNameDict[concludeId]      #逆向关系图

def dialog_judge(lawGraphDict, currentNode):
    """
    对话判断主流程
    """
    if not idNumberDict.has_key(currentNode):
        print currentNode
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

"""
1）映射：
    偷|偷盗-》窃取

"""
def match_pattern(inquiryStr, stateSlot):
    """
    获取用户话语中的关键信息，未完成
    目前支持：
        1）提取金额
    """
    inquiryStr = u"盗窃1000元钱也构成犯罪吗"
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
    response = response.decode('gbk').encode('utf8')
    if answerType == 'yes_or_not':
        if response == 'yes':
            return True
        else:
            return False
    elif answerType == 'condition':
        if isStatisfyState in response:
            return True
        else:
            return False


def query_slot(slotState, isStatisfyState):
    """
    客观条件和主观条件的所有状态询问，未完成
    目前有两种询问方法：
        1）是否
        2）条件询问（如对"地点"的询问）
    """
    if slotState == u"事件阶段":
        if isStatisfyState == u'案发后':
            print u"请问事件阶段是否已经在案发后？\n"
        return solve_answer('yes_or_not')
    if slotState == u"完成形态":
        if isStatisfyState == u'既遂':
            print u"请问您盗窃的物品是否脱离了被害人的控制？\n"
        return solve_answer('yes_or_not')
    if slotState == u"后果":
        for item in objSlot:
            if item == isStatisfyState:
                print u"请问您是否导致" + item
            return solve_answer('yes_or_not')
    if slotState == u"地点":
        print u"请问您当时所在的场所？"
        return solve_answer('yes_or_not')


def check_states_slot(atomicRule, stateSlot):
    subobjList = atomicRule.split('\t')
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
            slotState, isStatisfyState = read_slot([elem], objSlot)
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
    for key in objSlot:
        stateSlot[key] = set()

if __name__ == '__main__':
    states = ["45", "123"]
    nameElemDict = {}
    idNameDict = {}     #id到name的映射
    idNumberDict = {}       #id到要件序号的映射
    lawGraphDict = {}
    reverseGraphDict = {}       #关系逆向图
    subSlot = {}        #主观槽
    objSlot = {}        #客观槽
    stateSlot = {}      #状态槽
    wordMap = {u"窃取":[u"偷"]}        #关键词映射图
    read_factor(nameElemDict, idNameDict)
    read_rule(idNameDict, lawGraphDict, reverseGraphDict)
    InitSlot()

    #需要先提出几个通用问题，以减少规则匹配
    print u"您好，请问有什么需要帮助的吗？\n"
    #response = raw_input()
    #response = response.decode('gbk').encode('utf8')
    response = u"偷1000元钱也构成犯罪吗"
    fill_slot(response, stateSlot)
    if u"窃取" in stateSlot[u"行为"]:
        print u"还偷了其他物品吗\n"     #通用问题一
    response = u"还有信用卡"
    fill_slot(response, stateSlot)
    if u"窃取" in stateSlot[u"行为"]:
        result = dialog_judge(lawGraphDict, "客体及客观方面")
    else:
        result = True
    if result:
        #print "你犯了盗窃罪"
        print "YES"
    else:
        #print "你没有犯盗窃罪"
        print "NO"

    """
    添加“还有什么需要补充的吗？，承接其他罪名判断”
    """
