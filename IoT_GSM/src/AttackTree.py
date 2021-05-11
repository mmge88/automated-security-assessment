"""
CREST Project 9: Automated security assessment for interconnected systems
Created by Mengmeng Ge
Modified by Moyang Feng
05/02/2020
This module constructs attack tree.
"""

from Node import *
from Network import *
from Vulnerability import *


class tNode(node):
    """
    Create attack tree node object.
    """
    def __init__(self, name):
        super(tNode, self).__init__(name)
        self.n = None
        self.t = "node"
        self.val = 0
        self.mv2 = metrics_v2()
    
    def __str__(self):
        return self.name

class tVulNode(vulNode):
    """
    Create attack tree vulnerability object.
    """
    def __init__(self, name):
        super(tVulNode, self).__init__(name)
        self.n = None
        self.t = "node"
        self.val = 0
        self.command = 0
        self.mv2 = metrics_v2()
        
    def __str__(self):
        return self.name
      
class andGate(node):
    def __init__(self):
        super(andGate, self).__init__("andGate")
        self.t = "andGate"

class orGate(node):
    def __init__(self):
        super(orGate, self).__init__("orGate")
        self.t = "orGate"

     
class at(object):
    """
    Create attack tree.
    """
    def __init__(self, network, val, *arg):
        self.nodes = []
        self.topGate = None
        self.construct(network, val, *arg)
        self.isAG = 0
    
    #Preprocess for the construction
    def preprocess(self, network, nodes, val, *arg):  
        for u in [network.start, network.end] + network.nodes:
            if u is not None:
                #For vulNode
                if type(u) is vulNode:
                    tn = tVulNode('at_'+str(u.name))
                    tn.privilege = u.privilege
                    tn.mv2 = u.mv2
                    tn.vulname = u.name
                #For node
                else:
                    tn = tNode('at_'+str(u.name))
                    
                    #Assign default value to attacker node
                    if u.isStart == True:
                        tn.val = -1
                    else:
                        tn.val = val
                    
                tn.n = u
                
                #Assign default value to start and end in vulnerability network
                if u in [network.start, network.end]:
                    tn.val = 0
                    tn.command = 1
                    
                nodes.append(tn)   
        
        #Initialize connections for attack tree node
        # tnode
        for u in nodes:
            # vulNode
            for v in u.n.connections:
                #For upper layer
                if len(arg) is 0:
                    # tNode
                    for t in nodes:
                        if t.n is v:
                            u.connections.append(t)
                #For lower layer
                else:
                    # Privilege value is used here to decide what vulnerabilities an attacker can use for attack paths 
                    if v.privilege is not None and arg[0] >= v.privilege:
                        for t in nodes:
                            if t.n is v:
                                u.connections.append(t)      
        return None
    
    #Construct the attack tree
    def construct(self, network, val, *arg):
        nodes = []      # tNode/tVulNode
        history = []
        e = None
        self.topGate = orGate()
        self.preprocess(network, nodes, val, *arg)

        #For one vulnerability
        if len(nodes) < 4:
            a_gate = andGate()
            for node in nodes:
                a_gate.connections.append(node)
                
            self.topGate.connections.append(a_gate)
        #For more than one vulnerability
        else:
            for u in nodes:
                if u.n is network.end:
                    e = u
                if u.n is network.start:
                    self.topGate.connections.append(u)
            
            self.simplify(self.topGate, history, e)
            self.targetOut(self.topGate, e)
            self.foldgate(self.topGate)

    #Simplify the method
    def simplify(self, gate, history, target):
        tGate = []
        tGate.extend(gate.connections)
        value = 1
        if len(tGate) == 0:
            value = 0
        
        for item in tGate:    
            if (item is not target) and (item.t is "node"):
                a_gate = andGate()
                gate.connections.append(a_gate)
                gate.connections.remove(item)
                                          
                a_gate.connections.append(item)
                o_gate = orGate()                                      
                a_gate.connections.append(o_gate)
                
                for u in item.connections:
                    if u not in history:
                        o_gate.connections.append(u)
                       
                history.append(item)
                value = self.simplify(o_gate, history, target)
                history.pop()
                if len(o_gate.connections) < 1:
                    a_gate.connections.remove(o_gate)
                    if len(a_gate.connections) == 1 and value == 0:
                        gate.connections.append(item)
                        gate.connections.remove(a_gate)
                
                value = value * item.val
    
        return value
    
    def targetOut(self, rootGate, target):
        self.targetOutRecursive(rootGate, target)
        for gate in rootGate.connections:
            gate.connections.append(target)
        self.deleteEmptyGates(rootGate)        
        
    def deleteEmptyGates(self, gate):
        removedGates = []
        for node in gate.connections:
            if node.t in ['andGate', 'orGate']:
                if (len(node.connections) is 1) and (node.connections[0] is "removed"):
                    removedGates.append(node)
                else:
                    self.deleteEmptyGates(node)
                                
        for node in removedGates:
            gate.connections.remove(node)    
                
    def targetOutRecursive(self, gate, target):
        toChange = []
        for node in gate.connections:
            if node is target:
                if len(gate.connections) is 1:
                    del gate.connections[:]
                    gate.connections.append("removed")
                    break
                else:                    
                    toChange.append(node)                    
                    
            elif node.t in ['andGate', 'orGate']:
                self.targetOutRecursive(node, target)
        for node in toChange:
            gate.connections.remove(node)
            nothing = tNode('at-.')
            nothing.val = 1            
            gate.connections.append(nothing)
            
    #Fold gate with one child                
    def foldgate(self, gate):
        removedGates = []
        for node in gate.connections:
            if node.t in ['andGate', 'orGate']:
                self.foldgate(node)
                if len(node.connections) == 1:
                    gate.connections.extend(node.connections)
                    removedGates.append(node)                
        for node in removedGates:
            gate.connections.remove(node)
            
    def tPrintRecursive(self, gate):
        print(gate.name, '->',)
        for u in gate.connections:
            print(u.name)
        print
        for u in gate.connections:
            if u.t in ['andGate', 'orGate']:
                self.tPrintRecursive(u)
    
    #Print tree
    def treePrint(self):
        self.tPrintRecursive(self.topGate)


    #---------------------------------------------------------------------------------------------------------------------------
    #Security analysis part: including attack impact, attack cost, return-on-attack, risk and attack success probability


    #---------------------------------------------------------------------------------------------------------------------------  
    #AT is upper layer
    #Assign child value to node value recursively

    def getBaseScoreRecursive(self, gate):
        for u in gate.connections:
            if u.t is "node":
                if u.child is not None:
                    u.mv2.baseScore = u.child.calcBaseScore()
            else:
                self.getBaseScoreRecursive(u)
      
    def getBaseScore(self):
        self.getBaseScoreRecursive(self.topGate)

    def getImpactValueRecursive(self, gate):
        for u in gate.connections:
            if u.t is "node":
                if u.child is not None:
                    u.mv2.impactScore = u.child.calcImpact()
            else:
                self.getImpactValueRecursive(u)
      
    def getImpactValue(self):
        self.getImpactValueRecursive(self.topGate)

    def getProValueRecursive(self, gate):
        for u in gate.connections:
            if u.t is "node": 
                if u.child is not None:                
                    u.mv2.probability = u.child.calcPro()
            else:
                self.getProValueRecursive(u)
    
    def getProValue(self):
        self.getProValueRecursive(self.topGate)

    def getRiskRecursive(self, gate):
        for u in gate.connections:
            if u.t is "node": 
                if u.child is not None:                
                    u.mv2.risk = u.child.calcRisk()
            else:
                self.getRiskRecursive(u)
    
    def getRisk(self):
        self.getRiskRecursive(self.topGate)

    #----------------------------------------------------------------------------------------------    
    #AT is lower layer

    #Calculate the base score for each node in the attack tree
    def calcBaseScoreRecursive(self, s):    
        if s.t is "andGate":
            val = 0
            for u in s.connections:                
                val += self.calcBaseScoreRecursive(u) 
                #print ('and: ', val)
        elif s.t is "orGate":
            val = 0
            for u in s.connections:
                tval = self.calcBaseScoreRecursive(u)
                if tval >= val:
                    val = tval 
                    #print('or:', val)
        elif s.t is "node":
            val = s.mv2.baseScore
            #print('node value: ', val, s.name)
        else:
            val = 0
        return val
    
    #Get the base score of each node in the attack tree
    def calcBaseScore(self):
        return self.calcBaseScoreRecursive(self.topGate)
   
    #Calculate the impact value for each node in the attack tree
    def calcImpactRecursive(self, s):    
        if s.t is "andGate":
            val = 0
            for u in s.connections:                
                val += self.calcImpactRecursive(u) 
                #print ('and: ', val)
        elif s.t is "orGate":
            val = 0
            for u in s.connections:
                tval = self.calcImpactRecursive(u)
                if tval >= val:
                    val = tval 
                    #print('or:', val)
        elif s.t is "node":
            val = s.mv2.impactScore
            #print('node value: ', val, s.name)
        else:
            val = 0
        return val
    
    #Get the impact value of each node in the attack tree
    def calcImpact(self):
        return self.calcImpactRecursive(self.topGate)

    #Calculate the probability value for each node in the attack tree
    def calcProRecursive(self, s):      
        if s.t is "andGate":
            val = 1.0
            for u in s.connections:
                val *= self.calcProRecursive(u) #probability
                print('and: ', val)
        elif s.t is "orGate":
            val = 1.0
            for u in s.connections:
                tval = self.calcProRecursive(u)
                #print('tval: ', tval)
                if tval > 0:
                    val *= (1.0-self.calcProRecursive(u)) #probability
            val = 1.0-val
            #print('or: ', val)
        elif s.t is "node" and s.mv2.probability > 0:
            val = s.mv2.probability
            #print('node: ', val, s.name)
        else:
            val = 1.0
        return val

    #Get the probability value of each node in the attack tree
    def calcPro(self):
        return self.calcProRecursive(self.topGate)


    #Calculate the risk value for each node in the attack tree
    def calcRiskRecursive(self, s):    
        if s.t is "andGate":
            val = 0
            for u in s.connections:                
                val += self.calcRiskRecursive(u) 
                #print ('and:', val)
        elif s.t is "orGate":
            val = 0
            for u in s.connections:
                tval = self.calcRiskRecursive(u)
                if tval >= val:
                    val = tval 
        elif s.t is "node":
            val = s.mv2.risk
        else:
            val = 0
        return val
    
    #Get the risk value of each node in the attack tree
    def calcRisk(self):
        return self.calcRiskRecursive(self.topGate)

    #When only one node is in the attack tree, calculate the value for the node
    def getNodeValue(self, s):    
        if s.t is "andGate":
            val = 0
            for u in s.connections:                
                val = self.getNodeValue(u) 
        elif s.t is "orGate":
            val = 0
            for u in s.connections:
                val = self.getNodeValue(u)
        elif s.t is "node":
            val = s.val
        else:
            val = 0
        return val

    #For MTTC
    #Get value recursively
    def getValueRecursive(self, gate, elements):
        for u in gate.connections:
            if u.t is "node": 
                if u.val > 0:
                    elements.append((u.name, u.val))
                #print (elements)
            else:
                self.getValueRecursive(u, elements)
        return None

    #Get gate type recursively
    def getGateRecursive(self, gate, orn, andn):
        for u in gate.connections:
            if u.t is 'orGate': 
                orn = orn + 1
                #print (u.name, orn)
                orn, andn = self.getGateRecursive(u, orn, andn)
            elif u.t is 'andGate':
                andn = andn + 1
                #print (u.name, andn)
                orn, andn = self.getGateRecursive(u, orn, andn)
        return (orn, andn)