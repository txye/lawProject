#encoding: utf-8  
from transitions import Machine
import re

class Element(object):
    def __init__(self, elemId, elemName, elemPrio):
        self.elemId = elemId
        self.elemName = elemName
        self.elemPrio = elemPrio

class Rule(object):
    def __init__(self, ruleName, ruleNum, listElem, logicRelation):
        self.ruleName = ruleName
        self.ruleNum = ruleNum
        self.listElem = listElem
        self.logicRelation = logicRelation

'''                
class Matter(object):
        states=['solid', 'liquid', 'gas', 'plasma']
        
        def __init__(self):
                self.machine = Machine(model=self, states=Matter.states, initial='solid')
                
                self.machine.add_transition('heat', 'solid', 'gas', conditions='is_flammable')
                self.machine.add_transition('heat2', 'solid', 'liquid', conditions=['is_really_hot'])
                
                
        def is_flammable(self): return False
        def is_really_hot(self): return True
    
#Test
test = Matter()
print test.heat()
'''
class Matter(object):
    states = []
    def __init__(self):
        self.machine = Machine(model=self, states=Matter.states, initial='主体')
    def is_and(self, elemPre, elemNow):
         pass
        
        
graph = Matter()
                
#elem = Element('其他亲属不予追究', 5);
#dict = {'http://classiclaw.com/resource/FACTOR-ac782c466dc77aeee96a6dec2c7fb7bd':elem}
#print dict['http://classiclaw.com/resource/FACTOR-ac782c466dc77aeee96a6dec2c7fb7bd'].elemPrio
file = open("factor.ttl")
states = []
while 1:
    line = file.readline()
    if not line:
        break
    match = re.match(r'<(\S+)>', line)
    if match:
        if 'elemId' in locals().keys(): 
            Elem = Element(elemId, elemName, elemPrio)
            states.append(Elem);
        elemId = match.group(1)
        continue
    match = re.match(ur'\s+Law:要件名\s+\"(\S+)\".*', line.decode('utf8'))
    if match:
        elemName =match.group(1)
        continue
    match = re.match(ur'\s+Law:要件级别\s+\"(\d+)\".*', line.decode('utf8'))
    if match:
        elemPrio =match.group(1)
            
#for i in states:
        #print i.elemName
        
file = open("rule.ttl")
while 1:
    line = file.readline()
    if not line:
        break
    if re.match(r'@.*', line):
        continue
    match = re.match(r'[^:]+:label\s+(\S+)', line)
    if match:
        ruleName =match.group(1)
        listElem = []
        continue
    match = re.match(r'\s+Law:\W+\s+\"(OR|AND)\".*', line)
    if match:
        logicRelation =match.group(1)
        continue
    match = re.match(ur'\s+Law:前提\s+<(\S+)>.*', line.decode('utf8'))
    if match:
        elemName =match.group(1)
        listElem.append(elemName)
        continue
    match = re.match(ur'\s+Law:结论\s+<(\S+)>.*', line.decode('utf8'))
    if match:
        concludeName =match.group(1)
        if logicRelation == 'AND':
            for i in range(len(listElem)):
                if(i == 0):
                    continue
                graph.machine.add_transition(logicRelation, listElem[i - 1], listElem[i], conditions='is_and')
            if len(listElem) > 0:
                graph.machine.add_transition(logicRelation, listElem[len(listElem) - 1], concludeName, conditions='is_and')
        else:
            for elem in listElem:
                graph.machine.add_transition(logicRelation, elem, concludeName)
        
                
                
                


