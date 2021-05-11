"""
CREST Project 9: Automated security assessment for interconnected systems
Created by Mengmeng Ge
Modified by Moyang Feng
05/02/2020
This module contains network object and relevant functions.
"""

from Node import *
from Topology import *
import copy

class network(object):
    """
    Create network object.
    """
    def __init__(self):
        self.name = ''
        #Initialize node list
        self.nodes = []     # vulNode/node
        #Initialize start and end points
        self.start = None
        self.end = None
        #Initialize subnets 
        self.subnets = []
        #Initialize vulnerability list which contains all node vulnerabilities
        self.vuls = []

    def copyNet(self):
        """
        Copy the network to a network.
        """
        
        temp = network()
        temp = copy.deepcopy(self)
        
        return temp
    
    def constructSE(self):
        """
        Set the start and end in the network.
        """
        self.start = node('S-')
        self.end = node('E-')
            
        for n in self.nodes:
            if n.isStart:
                self.start.connections.append(n)
            if n.isEnd:
                n.connections.append(self.end)
    
              
    def connectOneWay(self, node1, node2):
        """
        Connect node1 to node2 in the network.
        """
        #no self connection
        if node1 is node2:
            return None
        #connect node1 to node2
        if (node2 not in node1.connections):
            node1.connections.append(node2)    
      
    
    def connectTwoWays(self, node1, node2):
        """
        Connect node1 with node2 in the network.
        """
        #no self connection
        if node1 is node2:
            return None
        #create connections
        if (node2 not in node1.connections):
            node1.connections.append(node2)
        if (node1 not in node2.connections):
            node2.connections.append(node1)
    
    def disconnectTwoWays(self, node1, node2):
        """
        Disconnect node1 and node2 in the network.
        """
        if node2 in node1.connections:
            node1.connections.remove(node2)   
        if node1 in node2.connections:
            node2.connections.remove(node1)  
     
    def printNet(self):
        """
        Print network.
        """
        print('Printing network nodes in %s:\n' %self.name)
        for node in self.nodes:
            print("=== " + node.name + " : " + node.type + " ===")
            print("Connections:",)
            for conNode in node.connections:
                print(" - " + conNode.name)
            print("-----------------------------")
        return None
    
    def printNetWithVul(self):
        """
        Print network with vulnerabilities.
        """
        print('Printing network nodes in %s:\n' %self.name)
        for node in self.nodes:
            print("=== " + node.name + " : " + node.type + " ===")
            print("Connections:",)
            for conNode in node.connections:
                if conNode.name == 'S-' or conNode.name == 'E-':
                    print(" - " + conNode.name)
                else:
                    print(" - " + conNode.name)      
            
            print("Vulnerability:",)
            if node.vul is not None:
                for vul in node.vul.nodes:
                    vul.printInfo()
            print("------------------------------")
    
        return None

    def setName(self, name):
        self.name = name