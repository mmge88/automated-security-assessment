"""
CREST Project 9: Automated security assessment for interconnected systems
Created by Moyang Feng
05/02/2020
This module contains the security metrics for a vulnerability.
"""

class metrics_v2(object):
    """
    Create metrics object for CVSS V2.
    """
    def __init__(self):
        
        '''
        # unused parameters
        self.version = ''
        self.vectorString = ''
        self.severity = ''
        self.userInteractionRequired = False
        '''
        # CVSS V2 security metrics
        self.confidentialityImpact = ''
        self.integrityImpact = ''
        self.availabilityImpact = ''
        self.accessVector = ''
        self.accessComplexity = ''
        self.authentication = ''
        self.obtainAllPrivilege = False
        self.obtainUserPrivilege = False
        self.obtainOtherPrivilege = False
        self.impactScore = 0.0
        self.exploitabilityScore = 0.0
        self.baseScore = 0.0

        # custom metrics
        self.probability = 0.0
        self.risk = 0.0
    
    def readCVSS(self, data):
        '''
        # unused parameters
        self.version = data['cvssV2_version']
        self.vectorString = data['cvssV2_vectorString']
        self.severity = data['cvssV2_severity']
        self.userInteractionRequired = str2bool(data['cvssV2_userInteractionRequired'])
        '''

        self.confidentialityImpact = data['cvssV2_confidentialityImpact']
        self.integrityImpact = data['cvssV2_integrityImpact']
        self.availabilityImpact = data['cvssV2_availabilityImpact']
        self.accessVector = data['cvssV2_accessVector']
        self.accessComplexity = data['cvssV2_accessComplexity']
        self.authentication = data['cvssV2_authentication']
        self.obtainAllPrivilege = str2bool(data['cvssV2_obtainAllPrivilege'])           # pri = 3
        self.obtainUserPrivilege = str2bool(data['cvssV2_obtainUserPrivilege'])         # pri = 2
        self.obtainOtherPrivilege = str2bool(data['cvssV2_obtainOtherPrivilege'])       # pri = 1
        self.impactScore = float(data['ImpactScore'])
        self.exploitabilityScore = float(data['ExploitabilityScore'])
        self.baseScore = float(data['BaseScore'])

        self.probability = self.exploitabilityScore / 10
        self.risk = self.probability * self.impactScore

    def printInfo(self):
        print('===== CVSS V2 =====')

        if self.isEmpty():
            print('N/A')
            return

        '''
        # unused paramters
        print('Version: ', self.version)
        print('Vector String: ', self.vectorString)
        print('Severity: ', self.severity)
        print('User Interaction Required: ', self.userInteractionRequired)
        '''

        print('Confidentiality Impact: ', self.confidentialityImpact)
        print('Integrity Impact: ', self.integrityImpact)
        print('Availability Impact: ', self.availabilityImpact)
        print('Access Vector: ', self.accessVector)
        print('Access Complexity:', self.accessComplexity)
        print('Authentication: ', self.authentication)
        print('Obtain All Privilege: ', self.obtainAllPrivilege)            #pri = 3
        print('Obtain User Privilege: ', self.obtainUserPrivilege)          #pri = 2
        print('Obtain Other Privilege: ', self.obtainOtherPrivilege)        #pri = 1
        print('Impact Score: ', self.impactScore)
        print('Exploitability Score: ', self.exploitabilityScore)
        print('Base Score: ', self.baseScore)

    def isEmpty(self):
        if self.baseScore == 0.0:
            return True
        return False

class metrics_v3(object):
    """
    Create metrics object for CVSS V3.
    """
    def __init__(self, data):
        self.version = data['cvssV3_version']
        if self.isEmpty():
            return
        
        self.vectorString = data['cvssV3_vectorString']
        self.attackVector = data['cvssV3_attackVector']
        self.attackComplexity = data['cvssV3_attackComplexity']
        self.privilegesRequired = data['cvssV3_privilegesRequired']
        self.userInteraction = data['cvssV3_userInteraction']
        self.scope = data['cvssV3_scope']
        self.confidentialityImpact = data['cvssV3_confidentialityImpact']
        self.integrityImpact = data['cvssV3_integrityImpact']
        self.availabilityImpact = data['cvssV3_availabilityImpact']
        self.baseScore = float(data['cvssV3_baseScore'])
        self.severity = data['cvssV3_baseSeverity']
        self.exploitabilityScore = float(data['cvssV3_exploitabilityScore'])
        self.impactScore = float(data['cvssV3_impactScore'])
        #self.acInsufInfo = str2bool(data['cvssV2_acInsufInfo'])

    def printInfo(self):
        print('===== CVSS V3 =====')

        if self.isEmpty():
            print('N/A')
            return

        print('Version: ', self.version)
        print('Vector String: ', self.vectorString)
        print('Attack Vector: ', self.attackVector)
        print('Attack Complexity:', self.attackComplexity)
        print('Privileges Required:', self.privilegesRequired)
        print('User Interaction:', self.userInteraction)
        print('Scope:', self.scope)
        print('Confidentiality Impact: ', self.confidentialityImpact)
        print('Integrity Impact: ', self.integrityImpact)
        print('Availability Impact: ', self.availabilityImpact)
        print('Base Score: ', self.baseScore)
        print('Severity: ', self.severity)
        print('Exploitability Score: ', self.exploitabilityScore)
        print('Impact Score: ', self.impactScore)
        #print('Ac Insuf Info: ', self.acInsufInfo)

    def isEmpty(self):
        if self.version == '':
            return True
        return False

def str2bool(str):
  return str.lower() == 'true'