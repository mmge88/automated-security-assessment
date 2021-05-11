"""
CREST Project 9: Automated security assessment for interconnected systems
Created by Mengmeng Ge
Modified by Moyang Feng
05/02/2020
This module generates example IoT networks based on topology type and vulnerabilities.
"""

from Network import *
from Vulnerability import *
from Harm import *
from SecurityEvaluator import *
import math
import csv
import os

"""
-------------------------------------------------------------------------
Create network with vulnerabilities for the example IoT network.
-------------------------------------------------------------------------
"""

# list of imported vulnerabilities
vuls_original = []
vuls_predicted = []

# Read vulnerability data from input CSV file
# path: absolute file path
# t: vulnerability type (1 - originl, 2 - predicted)
def input(path,t):

    with open(path,'r',encoding='UTF-8') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')
        vuls = []

        for row in csv_reader:
            vul = vulNode('')
            vul.readCVSS(row)
            vuls.append(vul)

    if t == 1:
        vuls_original.append(vuls)
        print('Imported %d original vulnerabilities from %s\n' %(len(vuls),path))
    elif t == 2:
        vuls_predicted.append(vuls)
        print('Imported %d predicted vulnerabilities from %s\n' %(len(vuls),path))
    else:
        print('Unrecognised type: input must be 1 - original / 2 - predicted\n')

    return None

# create a lighting system under wifi
def createLighting(vuls):

    # create 10 lights
    lights = []
    for i in range(2):
        light = iot('light' + str(i))
        light.subnet.append('wifi')

        # assign two vulnerabilties from the imported list
        v00 = vuls[0][0]
        v00.createVuls(light)
        v00.thresholdPri(light,1)
        v00.terminalPri(light,1)

        v01 = vuls[0][1]
        v01.createVuls(light)
        v01.thresholdPri(light,1)
        v01.terminalPri(light,1)

        #The attacker needs to exploit both vulnerabilities to compromise the node
        light.vul.connectOneWay(light.vul.nodes[0], light.vul.nodes[1])

        lights.append(light)

    # create occupancy sensor
    occupancy_sensor = iot('occupancy_sensor')
    occupancy_sensor.subnet.append('wifi')
    v1 = vuls[1][1]
    v1.createVuls(occupancy_sensor)
    v1.thresholdPri(occupancy_sensor,1)
    v1.terminalPri(occupancy_sensor,1)

    # create brightness sensor
    brightness_sensor = iot('brightness_sensor')
    brightness_sensor.subnet.append('wifi')
    v2 = vuls[2][0]
    v2.createVuls(brightness_sensor)
    v2.thresholdPri(brightness_sensor,1)
    v2.terminalPri(brightness_sensor,1)

    # create a light controller
    light_controller = computer('light_controller')
    light_controller.subnet.append('wifi')
    v3 = vuls[2][1]
    v3.createVuls(light_controller)
    v3.thresholdPri(light_controller,1)
    v3.terminalPri(light_controller,1)

    # create a wifi network
    net = network()
    net.setName('Lighting System')

    # connect devices in mesh topology
    net.connectTwoWays(occupancy_sensor,brightness_sensor)
    net.connectTwoWays(light_controller,occupancy_sensor)
    net.connectTwoWays(light_controller,brightness_sensor)
    for i in range(len(lights)):
        net.connectTwoWays(lights[i],occupancy_sensor)
        net.connectTwoWays(lights[i],brightness_sensor)
        net.connectOneWay(lights[i],light_controller)
        for j in range(i + 1,len(lights)):
            net.connectTwoWays(lights[i],lights[j])
    
    net.nodes.extend(lights)
    net.nodes.append(occupancy_sensor)
    net.nodes.append(brightness_sensor)
    net.nodes.append(light_controller)

    # set an attacker computer
    attacker = computer('attacker')
    attacker.setStart()

    # link the attacker with devices
    for node in net.nodes:
        # set the light controller as target
        if node.name == 'light_controller':
            node.setEnd()
        else:
            attacker.connections.append(node)
    
    net.nodes.append(attacker)
    net.constructSE()
    net.printNet()

    return net

# create a security system under wifi
def createSecurity(vuls):

    # create an electronic entrance guard and assign two vulnerabilities
    entrance_guard = iot('entrance_guard')
    entrance_guard.subnet.append('wifi')
    v00 = vuls[0][0]
    v00.createVuls(entrance_guard)
    v00.thresholdPri(entrance_guard,1)
    v00.terminalPri(entrance_guard,1)
    v01 = vuls[0][1]
    v01.createVuls(entrance_guard)
    v01.thresholdPri(entrance_guard,1)
    v01.terminalPri(entrance_guard,1)
    #The attacker needs to exploit both vulnerabilities to compromise the node
    entrance_guard.vul.connectOneWay(entrance_guard.vul.nodes[0], entrance_guard.vul.nodes[1])

    # create a video surveillance device and assign three vulnerabilties
    surveillance = iot('surveillance')
    surveillance.subnet.append('wifi')
    v10 = vuls[1][0]
    v10.createVuls(surveillance)
    v10.thresholdPri(surveillance,1)
    v10.terminalPri(surveillance,1)
    v11 = vuls[1][1]
    v11.createVuls(surveillance)
    v11.thresholdPri(surveillance,1)
    v11.terminalPri(surveillance,1)
    v12 = vuls[1][2]
    v12.createVuls(surveillance)
    v12.thresholdPri(surveillance,1)
    v12.terminalPri(surveillance,1)
    #The attacker needs to exploit all vulnerabilities to compromise the node
    surveillance.vul.connectOneWay(surveillance.vul.nodes[0], surveillance.vul.nodes[1])
    surveillance.vul.connectOneWay(surveillance.vul.nodes[1], surveillance.vul.nodes[2])

    # create a burglar alarm and assign three vulnerabilties
    alarm = iot('alarm')
    alarm.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(alarm)
    v20.thresholdPri(alarm,1)
    v20.terminalPri(alarm,1)
    v21 = vuls[2][2]
    v21.createVuls(alarm)
    v21.thresholdPri(alarm,1)
    v21.terminalPri(alarm,1)
    v22 = vuls[2][3]
    v22.createVuls(alarm)
    v22.thresholdPri(alarm,1)
    v22.terminalPri(alarm,1)
    #The attacker needs to exploit all vulnerabilities to compromise the node
    alarm.vul.connectOneWay(alarm.vul.nodes[0], alarm.vul.nodes[1])
    alarm.vul.connectOneWay(alarm.vul.nodes[1], alarm.vul.nodes[2])

    # create a wifi network
    net = network()
    net.setName('Security System')

    # connect devices in mesh topology and add into the network
    net.connectTwoWays(entrance_guard,surveillance)
    net.connectTwoWays(entrance_guard,alarm)
    net.connectTwoWays(surveillance,alarm)
    net.nodes.append(entrance_guard)
    net.nodes.append(surveillance)
    net.nodes.append(alarm)

    # set an attacker computer
    attacker = computer('attacker')
    attacker.setStart()

    # link the attacker with devices
    for node in net.nodes:
        # set the entrance guard as target
        if node.name == 'entrance_guard':
            node.setEnd()
        else:
            attacker.connections.append(node)

    net.nodes.append(attacker)
    net.constructSE()
    net.printNet()

    return net

# create a HVAC system under wifi
def createHVAC(vuls):
    # create a humidity sensor and assign two vulnerabilities
    humidity_sensor = iot('humidity_sensor')
    humidity_sensor.subnet.append('wifi')
    v00 = vuls[0][0]
    v00.createVuls(humidity_sensor)
    v00.thresholdPri(humidity_sensor,1)
    v00.terminalPri(humidity_sensor,1)
    v01 = vuls[0][1]
    v01.createVuls(humidity_sensor)
    v01.thresholdPri(humidity_sensor,1)
    v01.terminalPri(humidity_sensor,1)
    #The attacker needs to exploit both vulnerabilities to compromise the node
    humidity_sensor.vul.connectOneWay(humidity_sensor.vul.nodes[0], humidity_sensor.vul.nodes[1])

    # create a ventilator and assign one vulnerability
    ventilator = iot('ventilator')
    ventilator.subnet.append('wifi')
    v10 = vuls[1][0]
    v10.createVuls(ventilator)
    v10.thresholdPri(ventilator,1)
    v10.terminalPri(ventilator,1)

    # create a CO2 sensor and assign two vulnerabilities
    CO2_sensor = iot('CO2_sensor')
    CO2_sensor.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(CO2_sensor)
    v20.thresholdPri(CO2_sensor,1)
    v20.terminalPri(CO2_sensor,1)
    v21 = vuls[2][1]
    v21.createVuls(CO2_sensor)
    v21.thresholdPri(CO2_sensor,1)
    v21.terminalPri(CO2_sensor,1)
    #The attacker needs to exploit both vulnerabilities to compromise the node
    CO2_sensor.vul.connectOneWay(CO2_sensor.vul.nodes[0], CO2_sensor.vul.nodes[1])

    # create a heater and assign two vulnerabilities
    heater = iot('heater')
    heater.subnet.append('wifi')
    v30 = vuls[3][0]
    v30.createVuls(heater)
    v30.thresholdPri(heater,1)
    v30.terminalPri(heater,1)
    v31 = vuls[3][1]
    v31.createVuls(heater)
    v31.thresholdPri(heater,1)
    v31.terminalPri(heater,1)
    #The attacker needs to exploit both vulnerabilities to compromise the node
    heater.vul.connectOneWay(heater.vul.nodes[0], heater.vul.nodes[1])

    # create a air conditioner and assign one vulnerability
    air_conditioner = iot('air_conditioner')
    air_conditioner.subnet.append('wifi')
    v40 = vuls[4][0]
    v40.createVuls(air_conditioner)
    v40.thresholdPri(air_conditioner,1)
    v40.terminalPri(air_conditioner,1)

    # create a thermometer and assign two vulnerabilities
    thermometer = iot('thermometer')
    thermometer.subnet.append('wifi')
    v50 = vuls[5][0]
    v50.createVuls(thermometer)
    v50.thresholdPri(thermometer,1)
    v50.terminalPri(thermometer,1)
    v51 = vuls[5][1]
    v51.createVuls(thermometer)
    v51.thresholdPri(thermometer,1)
    v51.terminalPri(thermometer,1)
    #The attacker needs to exploit both vulnerabilities to compromise the node
    thermometer.vul.connectOneWay(thermometer.vul.nodes[0], thermometer.vul.nodes[1])

    # create occupancy sensor and assign one vulnerability
    occupancy_sensor = iot('occupancy_sensor')
    occupancy_sensor.subnet.append('wifi')
    v60 = vuls[6][0]
    v60.createVuls(occupancy_sensor)
    v60.thresholdPri(occupancy_sensor,1)
    v60.terminalPri(occupancy_sensor,1)

    # create a wifi network
    net = network()
    net.setName('HVAC System')

    # connect devices as designed in the system model
    net.connectOneWay(humidity_sensor,ventilator)
    net.connectOneWay(CO2_sensor,ventilator)
    net.connectOneWay(humidity_sensor,heater)
    net.connectOneWay(humidity_sensor,air_conditioner)
    net.connectOneWay(thermometer,heater)
    net.connectOneWay(thermometer,air_conditioner)
    net.connectOneWay(occupancy_sensor,heater)
    net.connectOneWay(occupancy_sensor,air_conditioner)
    net.nodes.append(humidity_sensor)
    net.nodes.append(ventilator)
    net.nodes.append(CO2_sensor)
    net.nodes.append(heater)
    net.nodes.append(air_conditioner)
    net.nodes.append(thermometer)
    net.nodes.append(occupancy_sensor)

    # set an attacker computer
    attacker = computer('attacker')
    attacker.setStart()

    # link the attacker with devices
    for node in net.nodes:
        # set the heater, air conditioner and ventilator as targets
        if node.name in ['heater', 'air_conditioner','ventilator']:
            node.setEnd()
        else:
            attacker.connections.append(node)

    net.nodes.append(attacker)
    net.constructSE()
    net.printNet()

    return net

# create a audiovisual system under wifi
def createAudiovisual(vuls):
    # create a brightness sensor and assign two vulnerabilities
    brightness_sensor = iot('brightness_sensor')
    brightness_sensor.subnet.append('wifi')
    v00 = vuls[0][0]
    v00.createVuls(brightness_sensor)
    v00.thresholdPri(brightness_sensor,1)
    v00.terminalPri(brightness_sensor,1)
    v01 = vuls[0][1]
    v01.createVuls(brightness_sensor)
    v01.thresholdPri(brightness_sensor,1)
    v01.terminalPri(brightness_sensor,1)
    #The attacker needs to exploit both vulnerabilities to compromise the node
    brightness_sensor.vul.connectOneWay(brightness_sensor.vul.nodes[0], brightness_sensor.vul.nodes[1])

    # create a projector and assign one vulnerability
    projector = iot('projector')
    projector.subnet.append('wifi')
    v10 = vuls[1][0]
    v10.createVuls(projector)
    v10.thresholdPri(projector,1)
    v10.terminalPri(projector,1)

    # create a tv and assign one vulnerability
    tv = iot('tv')
    tv.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(tv)
    v20.thresholdPri(tv,1)
    v20.terminalPri(tv,1)

    # create a speaker and assign one vulnerability
    speaker = iot('speaker')
    speaker.subnet.append('wifi')
    v21 = vuls[2][1]
    v21.createVuls(speaker)
    v21.thresholdPri(speaker,1)
    v21.terminalPri(speaker,1)

    # create a wifi network
    net = network()
    net.setName('Audiovisual System')

    # connect devices as designed in the system model
    net.connectOneWay(brightness_sensor,projector)
    net.connectOneWay(brightness_sensor,tv)
    net.connectOneWay(projector,speaker)
    net.connectOneWay(tv,speaker)
    net.nodes.append(brightness_sensor)
    net.nodes.append(projector)
    net.nodes.append(tv)
    net.nodes.append(speaker)

    # set an attacker computer
    attacker = computer('attacker')
    attacker.setStart()

    # link the attacker with devices
    for node in net.nodes:
        # set the speaker as target
        if node.name == 'speaker':
            node.setEnd()
        else:
            attacker.connections.append(node)

    net.nodes.append(attacker)
    net.constructSE()
    net.printNet()

    return net

# create a fire detection system under wifi
def createFireDetection(vuls):
    # create a CO sensor and assign two vulnerabilities
    CO_sensor = iot('CO_sensor')
    CO_sensor.subnet.append('wifi')
    v00 = vuls[0][0]
    v00.createVuls(CO_sensor)
    v00.thresholdPri(CO_sensor,1)
    v00.terminalPri(CO_sensor,1)
    v01 = vuls[0][1]
    v01.createVuls(CO_sensor)
    v01.thresholdPri(CO_sensor,1)
    v01.terminalPri(CO_sensor,1)
    #The attacker needs to exploit both vulnerabilities to compromise the node
    CO_sensor.vul.connectOneWay(CO_sensor.vul.nodes[0], CO_sensor.vul.nodes[1])

    # create a thermometer and assign two vulnerabilities
    thermometer = iot('thermometer')
    thermometer.subnet.append('wifi')
    v10 = vuls[1][0]
    v10.createVuls(thermometer)
    v10.thresholdPri(thermometer,1)
    v10.terminalPri(thermometer,1)
    v11 = vuls[1][1]
    v11.createVuls(thermometer)
    v11.thresholdPri(thermometer,1)
    v11.terminalPri(thermometer,1)
    #The attacker needs to exploit both vulnerabilities to compromise the node
    thermometer.vul.connectOneWay(thermometer.vul.nodes[0], thermometer.vul.nodes[1])

    # create a fire alarm and assign four vulnerabilities
    # only need to exploit one of them to compromise the node
    fire_alarm = iot('fire_alarm')
    fire_alarm.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(fire_alarm)
    v20.thresholdPri(fire_alarm,1)
    v20.terminalPri(fire_alarm,1)
    v21 = vuls[2][1]
    v21.createVuls(fire_alarm)
    v21.thresholdPri(fire_alarm,1)
    v21.terminalPri(fire_alarm,1)
    v22 = vuls[2][2]
    v22.createVuls(fire_alarm)
    v22.thresholdPri(fire_alarm,1)
    v22.terminalPri(fire_alarm,1)
    v23 = vuls[2][3]
    v23.createVuls(fire_alarm)
    v23.thresholdPri(fire_alarm,1)
    v23.terminalPri(fire_alarm,1)

    # create a wifi network
    net = network()
    net.setName('Fire Detection System')

    # connect devices as designed in the system model
    net.connectOneWay(CO_sensor,fire_alarm)
    net.connectOneWay(thermometer,fire_alarm)
    net.nodes.append(CO_sensor)
    net.nodes.append(thermometer)
    net.nodes.append(fire_alarm)

    # set an attacker computer
    attacker = computer('attacker')
    attacker.setStart()

    # link the attacker with devices
    for node in net.nodes:
        # set the fire alarm as target
        if node.name == 'fire_alarm':
            node.setEnd()
        else:
            attacker.connections.append(node)

    net.nodes.append(attacker)
    net.constructSE()
    net.printNet()

    return net

# analyse probability of attack of the network using original and predicted vulnerabilities
# net_o: network constructed with original vulnerabilities
# net_p: network constructed with predicted vulnerabilities
# pri: assign a privilege value in construction of lower layer vulnerability connections
def analyseProbability(net_o,net_p,pri):
    pro_original,_,_ = attackProAnalysis(net_original,pri)
    pro_predicted,_,_ = attackProAnalysis(net_predicted,pri)

    per_err = (abs(pro_original - pro_predicted) / pro_original) * 100

    print('Orignal Probability: %.2f\nPredicted Probability: %.2f\nPercentage Error: %.2f%%\n' %(pro_original,pro_predicted,per_err))

# analyse impact of the network using original and predicted vulnerabilities
# net_o: network constructed with original vulnerabilities
# net_p: network constructed with predicted vulnerabilities
# pri: assign a privilege value in construction of lower layer vulnerability connections
def analyseImpact(net_o,net_p,pri):
    impact_original,_,_ = attackImpactAnalysis(net_original,pri)
    impact_predicted,_,_ = attackImpactAnalysis(net_predicted,pri)

    per_err = (abs(impact_original - impact_predicted) / impact_original) * 100

    print('Orignal Impact: %.2f\nPredicted Impact: %.2f\nPercentage Error: %.2f%%\n' %(impact_original,impact_predicted,per_err))

# analyse risk of the network using original and predicted vulnerabilities
# net_o: network constructed with original vulnerabilities
# net_p: network constructed with predicted vulnerabilities
# pri: assign a privilege value in construction of lower layer vulnerability connections
def analyseRisk(net_o,net_p,pri):
    risk_original,_,_ = riskAnalysis(net_original,pri)
    risk_predicted,_,_ = riskAnalysis(net_predicted,pri)

    per_err = (abs(risk_original - risk_predicted) / risk_original) * 100

    print('Orignal Risk: %.2f\nPredicted Risk: %.2f\nPercentage Error: %.2f%%\n' %(risk_original,risk_predicted,per_err))

# analyse base score of the network using original and predicted vulnerabilities
# net_o: network constructed with original vulnerabilities
# net_p: network constructed with predicted vulnerabilities
# pri: assign a privilege value in construction of lower layer vulnerability connections
def analyseBaseScore(net_o,net_p,pri):
    bs_original,_,_ = baseScoreAnalysis(net_original,pri)
    bs_predicted,_,_ = baseScoreAnalysis(net_predicted,pri)

    per_err = (abs(bs_original - bs_predicted) / bs_original) * 100

    print('Orignal Base Score: %.2f\nPredicted Base Score: %.2f\nPercentage Error: %.2f%%\n' %(bs_original,bs_predicted,per_err))

if __name__ == '__main__':

    print('\nCREST Project 9: Automated security assessment for interconnected systems')
    print('IoT Graphical Security Model\n')

    # file directories of original and predicted vulnerabiltiies
    dir_o = os.path.join(os.path.dirname(__file__),'../data/original/')
    dir_p = os.path.join(os.path.dirname(__file__),'../data/predicted/')

    # set file names corresponding to each sub-system design
    #file_names = ['Lights.csv','Occupancy sensor.csv','Brightness sensor.csv']                                                                          # Lighting system
    #file_names = ['Electronic entrance guard.csv','Video surveillance.csv','Burglar alarm.csv']                                                         # Security system
    #file_names = ['Humidity sensor.csv','Ventilator.csv','CO2 sensor.csv','Heater.csv','Air conditioner.csv','Thermometer.csv','Occupancy sensor.csv']  # HVAC system
    #file_names = ['Brightness sensor.csv','Screen projector.csv','Smart TV.csv']                                                                        # Audiovisual system
    file_names = ['CO sensor.csv','Thermometer.csv','Fire alarm.csv']                                                                                   # Fire Detection system

    # read .csv files and store as a matrix of vulnerabilties
    for file_name in file_names:
        input(os.path.realpath(dir_o + file_name),1)        # orignal vulnerabiltiies
        input(os.path.realpath(dir_p + file_name),2)        # predicted vulnerabiltiies

    '''
        Sample Networks
    '''

    # create a lighting system network
    #net_original = createLighting(vuls_original)
    #net_predicted = createLighting(vuls_predicted)

    # create a security system network
    #net_original = createSecurity(vuls_original)
    #net_predicted = createSecurity(vuls_predicted)

    # create a HVAC system network
    #net_original = createHVAC(vuls_original)
    #net_predicted = createHVAC(vuls_predicted)

    # create a audiovisual system network
    #net_original = createAudiovisual(vuls_original)
    #net_predicted = createAudiovisual(vuls_predicted)

    # create a audiovisual system network
    net_original = createFireDetection(vuls_original)
    net_predicted = createFireDetection(vuls_predicted)

    '''
        Security Metrics
    '''

    # analyse probability of attack
    #analyseProbability(net_original,net_predicted,3)

    # analyse impact of attack
    #analyseImpact(net_original,net_predicted,3)

    # analyse risk of attack
    #analyseRisk(net_original,net_predicted,3)

    # analyse CVSS base score
    analyseBaseScore(net_original,net_predicted,3)