"""
CREST Project 9: Automated security assessment for interconnected systems
Created by Mengmeng Ge
Modified by Moyang Feng
05/02/2020
This module contains topology object.
"""

class topology(object):
    """
    Create topology object.
    """   
    def __init__(self, topoType, nodeNo):
        topoType = topoType.lower()
        
        if topoType not in ['tree', 'partialmesh', 'fullmesh']:
            return None
        else :
            #Assign topology type
            self.topoType = topoType    
            #Assign node number   
            self.nodeNo = nodeNo