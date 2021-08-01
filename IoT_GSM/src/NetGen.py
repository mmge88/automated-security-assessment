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


def input(path, t):

    with open(path, 'r', encoding='UTF-8') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')
        vuls = []

        for row in csv_reader:
            vul = vulNode('')
            vul.readCVSS(row)
            vuls.append(vul)

    if t == 1:
        vuls_original.append(vuls)
        print('Imported %d original vulnerabilities from %s\n' %
              (len(vuls), path))
    elif t == 2:
        vuls_predicted.append(vuls)
        print('Imported %d predicted vulnerabilities from %s\n' %
              (len(vuls), path))
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
        v00.thresholdPri(light, 1)
        v00.terminalPri(light, 1)

        v01 = vuls[0][1]
        v01.createVuls(light)
        v01.thresholdPri(light, 1)
        v01.terminalPri(light, 1)

        # The attacker needs to exploit both vulnerabilities to compromise the node
        light.vul.connectOneWay(light.vul.nodes[0], light.vul.nodes[1])
        lights.append(light)

    # create occupancy sensor
    occupancy_sensor = iot('occupancy_sensor')
    occupancy_sensor.subnet.append('wifi')
    v10 = vuls[1][0]
    v10.createVuls(occupancy_sensor)
    v10.thresholdPri(occupancy_sensor, 1)
    v10.terminalPri(occupancy_sensor, 1)

    # create brightness sensor
    brightness_sensor = iot('brightness_sensor')
    brightness_sensor.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(brightness_sensor)
    v20.thresholdPri(brightness_sensor, 1)
    v20.terminalPri(brightness_sensor, 1)

    # create a light controller
    light_controller = computer('light_controller')
    light_controller.subnet.append('wifi')
    v30 = vuls[2][1]
    v30.createVuls(light_controller)
    v30.thresholdPri(light_controller, 1)
    v30.terminalPri(light_controller, 1)

    # create a motion sensor
    motion_sensor = iot('motion_sensor')
    motion_sensor.subnet.append('wifi')
    v40 = vuls[3][0]
    v40.createVuls(motion_sensor)
    v40.thresholdPri(motion_sensor, 1)
    v40.terminalPri(motion_sensor, 1)

    # create a wifi network
    net = network()
    net.setName('Lighting System')

    # connect devices in mesh topology
    net.connectTwoWays(occupancy_sensor, brightness_sensor)
    net.connectTwoWays(light_controller, occupancy_sensor)
    net.connectTwoWays(light_controller, brightness_sensor)
    net.connectOneWay(motion_sensor, occupancy_sensor)
    net.connectOneWay(motion_sensor, brightness_sensor)
    for i in range(len(lights)):
        net.connectTwoWays(lights[i], occupancy_sensor)
        net.connectTwoWays(lights[i], brightness_sensor)
        net.connectOneWay(lights[i], light_controller)
        for j in range(i + 1, len(lights)):
            net.connectTwoWays(lights[i], lights[j])

    net.nodes.extend(lights)
    net.nodes.append(occupancy_sensor)
    net.nodes.append(brightness_sensor)
    net.nodes.append(light_controller)
    net.nodes.append(motion_sensor)

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
    v00.thresholdPri(entrance_guard, 1)
    v00.terminalPri(entrance_guard, 1)
    v01 = vuls[0][1]
    v01.createVuls(entrance_guard)
    v01.thresholdPri(entrance_guard, 1)
    v01.terminalPri(entrance_guard, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    entrance_guard.vul.connectOneWay(
        entrance_guard.vul.nodes[0], entrance_guard.vul.nodes[1])

    # create a video surveillance device and assign three vulnerabilties
    surveillance = iot('surveillance')
    surveillance.subnet.append('wifi')
    v10 = vuls[1][0]
    v10.createVuls(surveillance)
    v10.thresholdPri(surveillance, 1)
    v10.terminalPri(surveillance, 1)
    v11 = vuls[1][1]
    v11.createVuls(surveillance)
    v11.thresholdPri(surveillance, 1)
    v11.terminalPri(surveillance, 1)
    v12 = vuls[1][2]
    v12.createVuls(surveillance)
    v12.thresholdPri(surveillance, 1)
    v12.terminalPri(surveillance, 1)
    # The attacker needs to exploit all vulnerabilities to compromise the node
    surveillance.vul.connectOneWay(
        surveillance.vul.nodes[0], surveillance.vul.nodes[1])
    surveillance.vul.connectOneWay(
        surveillance.vul.nodes[1], surveillance.vul.nodes[2])

    # create a burglar alarm and assign three vulnerabilties
    alarm = iot('alarm')
    alarm.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(alarm)
    v20.thresholdPri(alarm, 1)
    v20.terminalPri(alarm, 1)
    v21 = vuls[2][2]
    v21.createVuls(alarm)
    v21.thresholdPri(alarm, 1)
    v21.terminalPri(alarm, 1)
    v22 = vuls[2][3]
    v22.createVuls(alarm)
    v22.thresholdPri(alarm, 1)
    v22.terminalPri(alarm, 1)
    # The attacker needs to exploit all vulnerabilities to compromise the node
    alarm.vul.connectOneWay(alarm.vul.nodes[0], alarm.vul.nodes[1])
    alarm.vul.connectOneWay(alarm.vul.nodes[1], alarm.vul.nodes[2])

    # create 5 door window alarm sensor
    door_window_alarm_sensors = []
    for i in range(2):
        door_window_alarm_sensor = iot('door_window_alarm_sensor' + str(i))
        door_window_alarm_sensor.subnet.append('wifi')

        # assign two vulnerabilties from the imported list
        v30 = vuls[3][0]
        v30.createVuls(door_window_alarm_sensor)
        v30.thresholdPri(door_window_alarm_sensor, 1)
        v30.terminalPri(door_window_alarm_sensor, 1)

        v31 = vuls[3][1]
        v31.createVuls(door_window_alarm_sensor)
        v31.thresholdPri(door_window_alarm_sensor, 1)
        v31.terminalPri(door_window_alarm_sensor, 1)

        # The attacker needs to exploit both vulnerabilities to compromise the node
        door_window_alarm_sensor.vul.connectOneWay(
            door_window_alarm_sensor.vul.nodes[0], door_window_alarm_sensor.vul.nodes[1])

        door_window_alarm_sensors.append(door_window_alarm_sensor)

    # create a wifi network
    net = network()
    net.setName('Security System')

    # connect devices in mesh topology and add into the network
    net.connectTwoWays(entrance_guard, surveillance)
    net.connectTwoWays(entrance_guard, alarm)
    net.connectTwoWays(surveillance, alarm)
    for i in range(len(door_window_alarm_sensors)):
        net.connectTwoWays(door_window_alarm_sensors[i], alarm)
        for j in range(i + 1, len(door_window_alarm_sensors)):
            net.connectTwoWays(
                door_window_alarm_sensors[i], door_window_alarm_sensors[j])

    net.nodes.append(entrance_guard)
    net.nodes.append(surveillance)
    net.nodes.append(alarm)
    net.nodes.extend(door_window_alarm_sensors)

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
    v00.thresholdPri(humidity_sensor, 1)
    v00.terminalPri(humidity_sensor, 1)
    v01 = vuls[0][1]
    v01.createVuls(humidity_sensor)
    v01.thresholdPri(humidity_sensor, 1)
    v01.terminalPri(humidity_sensor, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    humidity_sensor.vul.connectOneWay(
        humidity_sensor.vul.nodes[0], humidity_sensor.vul.nodes[1])

    # create a ventilator and assign one vulnerability
    ventilator = iot('ventilator')
    ventilator.subnet.append('wifi')
    v10 = vuls[1][0]
    v10.createVuls(ventilator)
    v10.thresholdPri(ventilator, 1)
    v10.terminalPri(ventilator, 1)

    # create a CO2 sensor and assign two vulnerabilities
    CO2_sensor = iot('CO2_sensor')
    CO2_sensor.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(CO2_sensor)
    v20.thresholdPri(CO2_sensor, 1)
    v20.terminalPri(CO2_sensor, 1)
    v21 = vuls[2][1]
    v21.createVuls(CO2_sensor)
    v21.thresholdPri(CO2_sensor, 1)
    v21.terminalPri(CO2_sensor, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    CO2_sensor.vul.connectOneWay(
        CO2_sensor.vul.nodes[0], CO2_sensor.vul.nodes[1])

    # create a heater and assign two vulnerabilities
    heater = iot('heater')
    heater.subnet.append('wifi')
    v30 = vuls[3][0]
    v30.createVuls(heater)
    v30.thresholdPri(heater, 1)
    v30.terminalPri(heater, 1)
    v31 = vuls[3][1]
    v31.createVuls(heater)
    v31.thresholdPri(heater, 1)
    v31.terminalPri(heater, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    heater.vul.connectOneWay(heater.vul.nodes[0], heater.vul.nodes[1])

    # create a air conditioner and assign one vulnerability
    air_conditioner = iot('air_conditioner')
    air_conditioner.subnet.append('wifi')
    v40 = vuls[4][0]
    v40.createVuls(air_conditioner)
    v40.thresholdPri(air_conditioner, 1)
    v40.terminalPri(air_conditioner, 1)

    # create a thermometer and assign two vulnerabilities
    thermometer = iot('thermometer')
    thermometer.subnet.append('wifi')
    v50 = vuls[5][0]
    v50.createVuls(thermometer)
    v50.thresholdPri(thermometer, 1)
    v50.terminalPri(thermometer, 1)
    v51 = vuls[5][1]
    v51.createVuls(thermometer)
    v51.thresholdPri(thermometer, 1)
    v51.terminalPri(thermometer, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    thermometer.vul.connectOneWay(
        thermometer.vul.nodes[0], thermometer.vul.nodes[1])

    # create occupancy sensor and assign one vulnerability
    occupancy_sensor = iot('occupancy_sensor')
    occupancy_sensor.subnet.append('wifi')
    v60 = vuls[6][0]
    v60.createVuls(occupancy_sensor)
    v60.thresholdPri(occupancy_sensor, 1)
    v60.terminalPri(occupancy_sensor, 1)

    # create 5 window sensor
    window_sensors = []
    for i in range(2):
        window_sensor = iot('window_sensor' + str(i))
        window_sensor.subnet.append('wifi')

        # assign two vulnerabilties from the imported list
        v70 = vuls[7][0]
        v70.createVuls(window_sensor)
        v70.thresholdPri(window_sensor, 1)
        v70.terminalPri(window_sensor, 1)

        v71 = vuls[7][1]
        v71.createVuls(window_sensor)
        v71.thresholdPri(window_sensor, 1)
        v71.terminalPri(window_sensor, 1)

        # The attacker needs to exploit both vulnerabilities to compromise the node
        window_sensor.vul.connectOneWay(
            window_sensor.vul.nodes[0], window_sensor.vul.nodes[1])

        window_sensors.append(window_sensor)

    # create a wifi network
    net = network()
    net.setName('HVAC System')

    # connect devices as designed in the system model
    net.connectOneWay(humidity_sensor, ventilator)
    net.connectOneWay(CO2_sensor, ventilator)
    net.connectOneWay(humidity_sensor, heater)
    net.connectOneWay(humidity_sensor, air_conditioner)
    net.connectOneWay(thermometer, heater)
    net.connectOneWay(thermometer, air_conditioner)
    net.connectOneWay(occupancy_sensor, heater)
    net.connectOneWay(occupancy_sensor, air_conditioner)
    for i in range(len(window_sensors)):
        net.connectOneWay(window_sensors[i], heater)
        net.connectOneWay(window_sensors[i], air_conditioner)
        for j in range(i + 1, len(window_sensors)):
            net.connectTwoWays(window_sensors[i], window_sensors[j])
    net.nodes.append(humidity_sensor)
    net.nodes.append(ventilator)
    net.nodes.append(CO2_sensor)
    net.nodes.append(heater)
    net.nodes.append(air_conditioner)
    net.nodes.append(thermometer)
    net.nodes.append(occupancy_sensor)
    net.nodes.extend(window_sensors)

    # set an attacker computer
    attacker = computer('attacker')
    attacker.setStart()

    # link the attacker with devices
    for node in net.nodes:
        # set the heater, air conditioner and ventilator as targets
        if node.name in ['heater', 'air_conditioner', 'ventilator']:
            node.setEnd()
        else:
            attacker.connections.append(node)

    net.nodes.append(attacker)
    net.constructSE()
    net.printNet()

    return net

# create a audiovisual system under wifi


def createAudiovisual(vuls):
    # create a media player and assign two vulnerabilities
    media_player = iot('media_player')
    media_player.subnet.append('wifi')
    v00 = vuls[0][0]
    v00.createVuls(media_player)
    v00.thresholdPri(media_player, 1)
    v00.terminalPri(media_player, 1)
    v01 = vuls[0][1]
    v01.createVuls(media_player)
    v01.thresholdPri(media_player, 1)
    v01.terminalPri(media_player, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    media_player.vul.connectOneWay(
        media_player.vul.nodes[0], media_player.vul.nodes[1])

    # create a projector and assign one vulnerability
    projector = iot('projector')
    projector.subnet.append('wifi')
    v10 = vuls[1][0]
    v10.createVuls(projector)
    v10.thresholdPri(projector, 1)
    v10.terminalPri(projector, 1)

    # create a tv and assign one vulnerability
    tv = iot('tv')
    tv.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(tv)
    v20.thresholdPri(tv, 1)
    v20.terminalPri(tv, 1)

    # create a speaker and assign one vulnerability
    speaker = iot('speaker')
    speaker.subnet.append('wifi')
    v21 = vuls[2][1]
    v21.createVuls(speaker)
    v21.thresholdPri(speaker, 1)
    v21.terminalPri(speaker, 1)

    # create a brightness sensor and assign two vulnerabilities
    brightness_sensor = iot('brightness_sensor')
    brightness_sensor.subnet.append('wifi')
    v30 = vuls[3][0]
    v30.createVuls(brightness_sensor)
    v30.thresholdPri(brightness_sensor, 1)
    v30.terminalPri(brightness_sensor, 1)
    v31 = vuls[3][1]
    v31.createVuls(brightness_sensor)
    v31.thresholdPri(brightness_sensor, 1)
    v31.terminalPri(brightness_sensor, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    brightness_sensor.vul.connectOneWay(
        brightness_sensor.vul.nodes[0], brightness_sensor.vul.nodes[1])

    # create a wifi network
    net = network()
    net.setName('Audiovisual System')

    # connect devices as designed in the system model
    net.connectOneWay(media_player, projector)
    net.connectOneWay(media_player, tv)
    net.connectOneWay(media_player, brightness_sensor)
    net.connectOneWay(projector, speaker)
    net.connectOneWay(tv, speaker)
    net.nodes.append(media_player)
    net.nodes.append(projector)
    net.nodes.append(tv)
    net.nodes.append(speaker)
    net.nodes.append(brightness_sensor)

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
    v00.thresholdPri(CO_sensor, 1)
    v00.terminalPri(CO_sensor, 1)
    v01 = vuls[0][1]
    v01.createVuls(CO_sensor)
    v01.thresholdPri(CO_sensor, 1)
    v01.terminalPri(CO_sensor, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    CO_sensor.vul.connectOneWay(CO_sensor.vul.nodes[0], CO_sensor.vul.nodes[1])

    # create a thermometer and assign two vulnerabilities
    thermometer = iot('thermometer')
    thermometer.subnet.append('wifi')
    v10 = vuls[1][0]
    v10.createVuls(thermometer)
    v10.thresholdPri(thermometer, 1)
    v10.terminalPri(thermometer, 1)
    v11 = vuls[1][1]
    v11.createVuls(thermometer)
    v11.thresholdPri(thermometer, 1)
    v11.terminalPri(thermometer, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    thermometer.vul.connectOneWay(
        thermometer.vul.nodes[0], thermometer.vul.nodes[1])

    # create a fire alarm and assign four vulnerabilities
    # only need to exploit one of them to compromise the node
    fire_alarm = iot('fire_alarm')
    fire_alarm.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(fire_alarm)
    v20.thresholdPri(fire_alarm, 1)
    v20.terminalPri(fire_alarm, 1)
    v21 = vuls[2][1]
    v21.createVuls(fire_alarm)
    v21.thresholdPri(fire_alarm, 1)
    v21.terminalPri(fire_alarm, 1)
    v22 = vuls[2][2]
    v22.createVuls(fire_alarm)
    v22.thresholdPri(fire_alarm, 1)
    v22.terminalPri(fire_alarm, 1)
    v23 = vuls[2][3]
    v23.createVuls(fire_alarm)
    v23.thresholdPri(fire_alarm, 1)
    v23.terminalPri(fire_alarm, 1)

    # create a smoke sensor and assign two vulnerabilities
    smoke_sensor = iot('smoke_sensor')
    smoke_sensor.subnet.append('wifi')
    v30 = vuls[3][0]
    v30.createVuls(smoke_sensor)
    v30.thresholdPri(smoke_sensor, 1)
    v30.terminalPri(smoke_sensor, 1)
    v31 = vuls[3][1]
    v31.createVuls(smoke_sensor)
    v31.thresholdPri(smoke_sensor, 1)
    v31.terminalPri(smoke_sensor, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    smoke_sensor.vul.connectOneWay(
        smoke_sensor.vul.nodes[0], smoke_sensor.vul.nodes[1])

    # create a wifi network
    net = network()
    net.setName('Fire Detection System')

    # connect devices as designed in the system model
    net.connectOneWay(CO_sensor, fire_alarm)
    net.connectOneWay(thermometer, fire_alarm)
    net.connectOneWay(smoke_sensor, fire_alarm)
    net.nodes.append(CO_sensor)
    net.nodes.append(thermometer)
    net.nodes.append(fire_alarm)
    net.nodes.append(smoke_sensor)

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

# create a resources tracking system under wifi


def createResourcesTracking(vuls):
    # create 10 asset tag
    asset_tags = []
    for i in range(2):
        asset_tag = iot('asset_tag' + str(i))
        asset_tag.subnet.append('wifi')

        # assign two vulnerabilties from the imported list
        v00 = vuls[0][0]
        v00.createVuls(asset_tag)
        v00.thresholdPri(asset_tag, 1)
        v00.terminalPri(asset_tag, 1)

        v01 = vuls[0][1]
        v01.createVuls(asset_tag)
        v01.thresholdPri(asset_tag, 1)
        v01.terminalPri(asset_tag, 1)

        # The attacker needs to exploit both vulnerabilities to compromise the node
        asset_tag.vul.connectOneWay(
            asset_tag.vul.nodes[0], asset_tag.vul.nodes[1])

        asset_tags.append(asset_tag)

    # create 10 wearable devices
    wearable_devices = []
    for i in range(2):
        wearable_device = iot('wearable_device' + str(i))
        wearable_device.subnet.append('wifi')

        # assign two vulnerabilties from the imported list
        # only need to exploit one of them to compromise the node
        v10 = vuls[1][0]
        v10.createVuls(wearable_device)
        v10.thresholdPri(wearable_device, 1)
        v10.terminalPri(wearable_device, 1)
        v11 = vuls[1][1]
        v11.createVuls(wearable_device)
        v11.thresholdPri(wearable_device, 1)
        v11.terminalPri(wearable_device, 1)

        wearable_devices.append(wearable_device)

    # create a burglar alarm and assign three vulnerabilties
    alarm = iot('alarm')
    alarm.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(alarm)
    v20.thresholdPri(alarm, 1)
    v20.terminalPri(alarm, 1)
    v21 = vuls[2][2]
    v21.createVuls(alarm)
    v21.thresholdPri(alarm, 1)
    v21.terminalPri(alarm, 1)
    v22 = vuls[2][3]
    v22.createVuls(alarm)
    v22.thresholdPri(alarm, 1)
    v22.terminalPri(alarm, 1)
    # The attacker needs to exploit all vulnerabilities to compromise the node
    alarm.vul.connectOneWay(alarm.vul.nodes[0], alarm.vul.nodes[1])
    alarm.vul.connectOneWay(alarm.vul.nodes[1], alarm.vul.nodes[2])

    # create a wifi network
    net = network()
    net.setName('Resources Tracking System')

    # connect devices as designed in the system model
    for i in range(len(asset_tags)):
        net.connectOneWay(asset_tags[i], alarm)
        for j in range(i + 1, len(asset_tags)):
            net.connectTwoWays(asset_tags[i], asset_tags[j])
    for i in range(len(wearable_devices)):
        net.connectOneWay(wearable_devices[i], alarm)
        for j in range(i + 1, len(wearable_devices)):
            net.connectTwoWays(wearable_devices[i], wearable_devices[j])
    net.nodes.extend(asset_tags)
    net.nodes.extend(wearable_devices)
    net.nodes.append(alarm)

    # set an attacker computer
    attacker = computer('attacker')
    attacker.setStart()

    # link the attacker with devices
    for node in net.nodes:
        # set the burglar alarm as target
        if node.name == 'alarm':
            node.setEnd()
        else:
            attacker.connections.append(node)

    net.nodes.append(attacker)
    net.constructSE()
    net.printNet()

    return net

# create a maintenance system under wifi


def createMaintenance(vuls):
    # create electrical current monitoring sensor and assign two vulnerabilities
    current_monitoring_sensor = iot('current_monitoring_sensor')
    current_monitoring_sensor.subnet.append('wifi')
    v00 = vuls[0][0]
    v00.createVuls(current_monitoring_sensor)
    v00.thresholdPri(current_monitoring_sensor, 1)
    v00.terminalPri(current_monitoring_sensor, 1)
    v01 = vuls[0][1]
    v01.createVuls(current_monitoring_sensor)
    v01.thresholdPri(current_monitoring_sensor, 1)
    v01.terminalPri(current_monitoring_sensor, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    current_monitoring_sensor.vul.connectOneWay(
        current_monitoring_sensor.vul.nodes[0], current_monitoring_sensor.vul.nodes[1])

    # create a water monitoring sensor and assign two vulnerabilities
    water_monitoring_sensor = iot('water_monitoring_sensor')
    water_monitoring_sensor.subnet.append('wifi')
    v10 = vuls[1][0]
    v10.createVuls(water_monitoring_sensor)
    v10.thresholdPri(water_monitoring_sensor, 1)
    v10.terminalPri(water_monitoring_sensor, 1)
    v11 = vuls[1][1]
    v11.createVuls(water_monitoring_sensor)
    v11.thresholdPri(water_monitoring_sensor, 1)
    v11.terminalPri(water_monitoring_sensor, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    water_monitoring_sensor.vul.connectOneWay(
        water_monitoring_sensor.vul.nodes[0], water_monitoring_sensor.vul.nodes[1])

    # create a repair alarm and assign two vulnerabilities
    # only need to exploit one of them to compromise the node
    alarm = iot('alarm')
    alarm.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(alarm)
    v20.thresholdPri(alarm, 1)
    v20.terminalPri(alarm, 1)
    v21 = vuls[2][1]
    v21.createVuls(alarm)
    v21.thresholdPri(alarm, 1)
    v21.terminalPri(alarm, 1)

    # create a wifi network
    net = network()
    net.setName('Maintenance System')

    # connect devices as designed in the system model
    net.connectOneWay(current_monitoring_sensor, alarm)
    net.connectOneWay(water_monitoring_sensor, alarm)
    net.nodes.append(current_monitoring_sensor)
    net.nodes.append(water_monitoring_sensor)
    net.nodes.append(alarm)

    # set an attacker computer
    attacker = computer('attacker')
    attacker.setStart()

    # link the attacker with devices
    for node in net.nodes:
        # set the fire alarm as target
        if node.name == 'alarm':
            node.setEnd()
        else:
            attacker.connections.append(node)

    net.nodes.append(attacker)
    net.constructSE()
    net.printNet()

    return net

# create a combined system of security system and resources tracking system under wifi


def createCombinedSecurityTracking(vuls):

    # create an electronic entrance guard and assign two vulnerabilities
    entrance_guard = iot('entrance_guard')
    entrance_guard.subnet.append('wifi')
    v00 = vuls[0][0]
    v00.createVuls(entrance_guard)
    v00.thresholdPri(entrance_guard, 1)
    v00.terminalPri(entrance_guard, 1)
    v01 = vuls[0][1]
    v01.createVuls(entrance_guard)
    v01.thresholdPri(entrance_guard, 1)
    v01.terminalPri(entrance_guard, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    entrance_guard.vul.connectOneWay(
        entrance_guard.vul.nodes[0], entrance_guard.vul.nodes[1])

    # create a video surveillance device and assign three vulnerabilties
    surveillance = iot('surveillance')
    surveillance.subnet.append('wifi')
    v10 = vuls[1][0]
    v10.createVuls(surveillance)
    v10.thresholdPri(surveillance, 1)
    v10.terminalPri(surveillance, 1)
    v11 = vuls[1][1]
    v11.createVuls(surveillance)
    v11.thresholdPri(surveillance, 1)
    v11.terminalPri(surveillance, 1)
    v12 = vuls[1][2]
    v12.createVuls(surveillance)
    v12.thresholdPri(surveillance, 1)
    v12.terminalPri(surveillance, 1)
    # The attacker needs to exploit all vulnerabilities to compromise the node
    surveillance.vul.connectOneWay(
        surveillance.vul.nodes[0], surveillance.vul.nodes[1])
    surveillance.vul.connectOneWay(
        surveillance.vul.nodes[1], surveillance.vul.nodes[2])

    # create a burglar alarm and assign three vulnerabilties
    alarm = iot('alarm')
    alarm.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(alarm)
    v20.thresholdPri(alarm, 1)
    v20.terminalPri(alarm, 1)
    v21 = vuls[2][2]
    v21.createVuls(alarm)
    v21.thresholdPri(alarm, 1)
    v21.terminalPri(alarm, 1)
    v22 = vuls[2][3]
    v22.createVuls(alarm)
    v22.thresholdPri(alarm, 1)
    v22.terminalPri(alarm, 1)
    # The attacker needs to exploit all vulnerabilities to compromise the node
    alarm.vul.connectOneWay(alarm.vul.nodes[0], alarm.vul.nodes[1])
    alarm.vul.connectOneWay(alarm.vul.nodes[1], alarm.vul.nodes[2])

    # create 5 door window alarm sensor
    door_window_alarm_sensors = []
    for i in range(2):
        door_window_alarm_sensor = iot('door_window_alarm_sensor' + str(i))
        door_window_alarm_sensor.subnet.append('wifi')

        # assign two vulnerabilties from the imported list
        v30 = vuls[3][0]
        v30.createVuls(door_window_alarm_sensor)
        v30.thresholdPri(door_window_alarm_sensor, 1)
        v30.terminalPri(door_window_alarm_sensor, 1)

        v31 = vuls[3][1]
        v31.createVuls(door_window_alarm_sensor)
        v31.thresholdPri(door_window_alarm_sensor, 1)
        v31.terminalPri(door_window_alarm_sensor, 1)

        # The attacker needs to exploit both vulnerabilities to compromise the node
        door_window_alarm_sensor.vul.connectOneWay(
            door_window_alarm_sensor.vul.nodes[0], door_window_alarm_sensor.vul.nodes[1])

        door_window_alarm_sensors.append(door_window_alarm_sensor)

    # create 10 asset tag
    asset_tags = []
    for i in range(2):
        asset_tag = iot('asset_tag' + str(i))
        asset_tag.subnet.append('wifi')

        # assign two vulnerabilties from the imported list
        v40 = vuls[4][0]
        v40.createVuls(asset_tag)
        v40.thresholdPri(asset_tag, 1)
        v40.terminalPri(asset_tag, 1)

        v41 = vuls[4][1]
        v41.createVuls(asset_tag)
        v41.thresholdPri(asset_tag, 1)
        v41.terminalPri(asset_tag, 1)

        # The attacker needs to exploit both vulnerabilities to compromise the node
        asset_tag.vul.connectOneWay(
            asset_tag.vul.nodes[0], asset_tag.vul.nodes[1])

        asset_tags.append(asset_tag)

    # create 10 wearable devices
    wearable_devices = []
    for i in range(2):
        wearable_device = iot('wearable_device' + str(i))
        wearable_device.subnet.append('wifi')

        # assign two vulnerabilties from the imported list
        # only need to exploit one of them to compromise the node
        v50 = vuls[5][0]
        v50.createVuls(wearable_device)
        v50.thresholdPri(wearable_device, 1)
        v50.terminalPri(wearable_device, 1)
        v51 = vuls[5][1]
        v51.createVuls(wearable_device)
        v51.thresholdPri(wearable_device, 1)
        v51.terminalPri(wearable_device, 1)

        wearable_devices.append(wearable_device)

    # create a wifi network
    net = network()
    net.setName('Combined Security Tracking System')

    # connect devices in mesh topology and add into the network
    net.connectTwoWays(entrance_guard, surveillance)
    net.connectTwoWays(entrance_guard, alarm)
    net.connectTwoWays(surveillance, alarm)
    for i in range(len(asset_tags)):
        net.connectOneWay(asset_tags[i], alarm)
        for j in range(i + 1, len(asset_tags)):
            net.connectTwoWays(asset_tags[i], asset_tags[j])
    for i in range(len(wearable_devices)):
        net.connectOneWay(wearable_devices[i], alarm)
        for j in range(i + 1, len(wearable_devices)):
            net.connectTwoWays(wearable_devices[i], wearable_devices[j])
    for i in range(len(door_window_alarm_sensors)):
        net.connectTwoWays(door_window_alarm_sensors[i], alarm)
        for j in range(i + 1, len(door_window_alarm_sensors)):
            net.connectTwoWays(
                door_window_alarm_sensors[i], door_window_alarm_sensors[j])

    net.nodes.append(entrance_guard)
    net.nodes.append(surveillance)
    net.nodes.append(alarm)
    net.nodes.extend(door_window_alarm_sensors)
    net.nodes.extend(asset_tags)
    net.nodes.extend(wearable_devices)

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


# create a combined system of audiovisual, lighting, fire detection, and HVAC system under wifi
def createCombinedALFH(vuls):
    # create a media player and assign two vulnerabilities
    media_player = iot('media_player')
    media_player.subnet.append('wifi')
    v00 = vuls[0][0]
    v00.createVuls(media_player)
    v00.thresholdPri(media_player, 1)
    v00.terminalPri(media_player, 1)
    v01 = vuls[0][1]
    v01.createVuls(media_player)
    v01.thresholdPri(media_player, 1)
    v01.terminalPri(media_player, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    media_player.vul.connectOneWay(
        media_player.vul.nodes[0], media_player.vul.nodes[1])

    # create a projector and assign one vulnerability
    projector = iot('projector')
    projector.subnet.append('wifi')
    v10 = vuls[1][0]
    v10.createVuls(projector)
    v10.thresholdPri(projector, 1)
    v10.terminalPri(projector, 1)

    # create a tv and assign one vulnerability
    tv = iot('tv')
    tv.subnet.append('wifi')
    v20 = vuls[2][0]
    v20.createVuls(tv)
    v20.thresholdPri(tv, 1)
    v20.terminalPri(tv, 1)

    # create a speaker and assign one vulnerability
    speaker = iot('speaker')
    speaker.subnet.append('wifi')
    v21 = vuls[2][1]
    v21.createVuls(speaker)
    v21.thresholdPri(speaker, 1)
    v21.terminalPri(speaker, 1)

    # create a brightness sensor and assign two vulnerabilities
    brightness_sensor = iot('brightness_sensor')
    brightness_sensor.subnet.append('wifi')
    v30 = vuls[3][0]
    v30.createVuls(brightness_sensor)
    v30.thresholdPri(brightness_sensor, 1)
    v30.terminalPri(brightness_sensor, 1)
    v31 = vuls[3][1]
    v31.createVuls(brightness_sensor)
    v31.thresholdPri(brightness_sensor, 1)
    v31.terminalPri(brightness_sensor, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    brightness_sensor.vul.connectOneWay(
        brightness_sensor.vul.nodes[0], brightness_sensor.vul.nodes[1])

 # create 10 lights
    lights = []
    for i in range(2):
        light = iot('light' + str(i))
        light.subnet.append('wifi')

        # assign two vulnerabilties from the imported list
        v40 = vuls[4][0]
        v40.createVuls(light)
        v40.thresholdPri(light, 1)
        v40.terminalPri(light, 1)

        v41 = vuls[4][1]
        v41.createVuls(light)
        v41.thresholdPri(light, 1)
        v41.terminalPri(light, 1)

        # The attacker needs to exploit both vulnerabilities to compromise the node
        light.vul.connectOneWay(light.vul.nodes[0], light.vul.nodes[1])
        lights.append(light)

    # create occupancy sensor
    occupancy_sensor = iot('occupancy_sensor')
    occupancy_sensor.subnet.append('wifi')
    v50 = vuls[5][0]
    v50.createVuls(occupancy_sensor)
    v50.thresholdPri(occupancy_sensor, 1)
    v50.terminalPri(occupancy_sensor, 1)

    # create a light controller
    light_controller = computer('light_controller')
    light_controller.subnet.append('wifi')
    v60 = vuls[6][1]
    v60.createVuls(light_controller)
    v60.thresholdPri(light_controller, 1)
    v60.terminalPri(light_controller, 1)

    # create a motion sensor
    motion_sensor = iot('motion_sensor')
    motion_sensor.subnet.append('wifi')
    v70 = vuls[7][0]
    v70.createVuls(motion_sensor)
    v70.thresholdPri(motion_sensor, 1)
    v70.terminalPri(motion_sensor, 1)

    # create a humidity sensor and assign two vulnerabilities
    humidity_sensor = iot('humidity_sensor')
    humidity_sensor.subnet.append('wifi')
    v80 = vuls[8][0]
    v80.createVuls(humidity_sensor)
    v80.thresholdPri(humidity_sensor, 1)
    v80.terminalPri(humidity_sensor, 1)
    v81 = vuls[8][1]
    v81.createVuls(humidity_sensor)
    v81.thresholdPri(humidity_sensor, 1)
    v81.terminalPri(humidity_sensor, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    humidity_sensor.vul.connectOneWay(
        humidity_sensor.vul.nodes[0], humidity_sensor.vul.nodes[1])

    # create a ventilator and assign one vulnerability
    ventilator = iot('ventilator')
    ventilator.subnet.append('wifi')
    v90 = vuls[9][0]
    v90.createVuls(ventilator)
    v90.thresholdPri(ventilator, 1)
    v90.terminalPri(ventilator, 1)

    # create a CO2 sensor and assign two vulnerabilities
    CO2_sensor = iot('CO2_sensor')
    CO2_sensor.subnet.append('wifi')
    v100 = vuls[10][0]
    v100.createVuls(CO2_sensor)
    v100.thresholdPri(CO2_sensor, 1)
    v100.terminalPri(CO2_sensor, 1)
    v101 = vuls[10][1]
    v101.createVuls(CO2_sensor)
    v101.thresholdPri(CO2_sensor, 1)
    v101.terminalPri(CO2_sensor, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    CO2_sensor.vul.connectOneWay(
        CO2_sensor.vul.nodes[0], CO2_sensor.vul.nodes[1])

    # create a heater and assign two vulnerabilities
    heater = iot('heater')
    heater.subnet.append('wifi')
    v110 = vuls[11][0]
    v110.createVuls(heater)
    v110.thresholdPri(heater, 1)
    v110.terminalPri(heater, 1)
    v111 = vuls[11][1]
    v111.createVuls(heater)
    v111.thresholdPri(heater, 1)
    v111.terminalPri(heater, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    heater.vul.connectOneWay(heater.vul.nodes[0], heater.vul.nodes[1])

    # create a air conditioner and assign one vulnerability
    air_conditioner = iot('air_conditioner')
    air_conditioner.subnet.append('wifi')
    v120 = vuls[12][0]
    v120.createVuls(air_conditioner)
    v120.thresholdPri(air_conditioner, 1)
    v120.terminalPri(air_conditioner, 1)

    # create a thermometer and assign two vulnerabilities
    thermometer = iot('thermometer')
    thermometer.subnet.append('wifi')
    v130 = vuls[13][0]
    v130.createVuls(thermometer)
    v130.thresholdPri(thermometer, 1)
    v130.terminalPri(thermometer, 1)
    v131 = vuls[13][1]
    v131.createVuls(thermometer)
    v131.thresholdPri(thermometer, 1)
    v131.terminalPri(thermometer, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    thermometer.vul.connectOneWay(
        thermometer.vul.nodes[0], thermometer.vul.nodes[1])

    # create 5 window sensor
    window_sensors = []
    for i in range(2):
        window_sensor = iot('window_sensor' + str(i))
        window_sensor.subnet.append('wifi')

        # assign two vulnerabilties from the imported list
        v140 = vuls[14][0]
        v140.createVuls(window_sensor)
        v140.thresholdPri(window_sensor, 1)
        v140.terminalPri(window_sensor, 1)

        v141 = vuls[14][1]
        v141.createVuls(window_sensor)
        v141.thresholdPri(window_sensor, 1)
        v141.terminalPri(window_sensor, 1)

        # The attacker needs to exploit both vulnerabilities to compromise the node
        window_sensor.vul.connectOneWay(
            window_sensor.vul.nodes[0], window_sensor.vul.nodes[1])

        window_sensors.append(window_sensor)

        # create a CO sensor and assign two vulnerabilities
    CO_sensor = iot('CO_sensor')
    CO_sensor.subnet.append('wifi')
    v150 = vuls[15][0]
    v150.createVuls(CO_sensor)
    v150.thresholdPri(CO_sensor, 1)
    v150.terminalPri(CO_sensor, 1)
    v151 = vuls[15][1]
    v151.createVuls(CO_sensor)
    v151.thresholdPri(CO_sensor, 1)
    v151.terminalPri(CO_sensor, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    CO_sensor.vul.connectOneWay(CO_sensor.vul.nodes[0], CO_sensor.vul.nodes[1])

    # create a fire alarm and assign four vulnerabilities
    # only need to exploit one of them to compromise the node
    fire_alarm = iot('fire_alarm')
    fire_alarm.subnet.append('wifi')
    v160 = vuls[16][0]
    v160.createVuls(fire_alarm)
    v160.thresholdPri(fire_alarm, 1)
    v160.terminalPri(fire_alarm, 1)
    v161 = vuls[16][1]
    v161.createVuls(fire_alarm)
    v161.thresholdPri(fire_alarm, 1)
    v161.terminalPri(fire_alarm, 1)
    v161 = vuls[16][2]
    v161.createVuls(fire_alarm)
    v161.thresholdPri(fire_alarm, 1)
    v161.terminalPri(fire_alarm, 1)
    v163 = vuls[16][3]
    v163.createVuls(fire_alarm)
    v163.thresholdPri(fire_alarm, 1)
    v163.terminalPri(fire_alarm, 1)

    # create a smoke sensor and assign two vulnerabilities
    smoke_sensor = iot('smoke_sensor')
    smoke_sensor.subnet.append('wifi')
    v170 = vuls[17][0]
    v170.createVuls(smoke_sensor)
    v170.thresholdPri(smoke_sensor, 1)
    v170.terminalPri(smoke_sensor, 1)
    v171 = vuls[17][1]
    v171.createVuls(smoke_sensor)
    v171.thresholdPri(smoke_sensor, 1)
    v171.terminalPri(smoke_sensor, 1)
    # The attacker needs to exploit both vulnerabilities to compromise the node
    smoke_sensor.vul.connectOneWay(
        smoke_sensor.vul.nodes[0], smoke_sensor.vul.nodes[1])

    # create a wifi network
    net = network()
    net.setName('Combined ALFH System')

    # connect devices as designed in the system model
    net.connectOneWay(media_player, projector)
    net.connectOneWay(media_player, tv)
    net.connectOneWay(media_player, brightness_sensor)
    net.connectOneWay(projector, speaker)
    net.connectOneWay(tv, speaker)
    net.connectTwoWays(occupancy_sensor, brightness_sensor)
    net.connectTwoWays(light_controller, occupancy_sensor)
    net.connectTwoWays(light_controller, brightness_sensor)
    net.connectOneWay(motion_sensor, occupancy_sensor)
    net.connectOneWay(motion_sensor, brightness_sensor)
    for i in range(len(lights)):
        net.connectTwoWays(lights[i], occupancy_sensor)
        net.connectTwoWays(lights[i], brightness_sensor)
        net.connectOneWay(lights[i], light_controller)
        for j in range(i + 1, len(lights)):
            net.connectTwoWays(lights[i], lights[j])
    net.connectOneWay(humidity_sensor, ventilator)
    net.connectOneWay(CO2_sensor, ventilator)
    net.connectOneWay(humidity_sensor, heater)
    net.connectOneWay(humidity_sensor, air_conditioner)
    net.connectOneWay(thermometer, heater)
    net.connectOneWay(thermometer, air_conditioner)
    net.connectOneWay(occupancy_sensor, heater)
    net.connectOneWay(occupancy_sensor, air_conditioner)
    for i in range(len(window_sensors)):
        net.connectOneWay(window_sensors[i], heater)
        net.connectOneWay(window_sensors[i], air_conditioner)
        for j in range(i + 1, len(window_sensors)):
            net.connectTwoWays(window_sensors[i], window_sensors[j])
    net.connectOneWay(CO_sensor, fire_alarm)
    net.connectOneWay(thermometer, fire_alarm)
    net.connectOneWay(smoke_sensor, fire_alarm)
    net.nodes.append(media_player)
    net.nodes.append(projector)
    net.nodes.append(tv)
    net.nodes.append(speaker)
    net.nodes.append(brightness_sensor)
    net.nodes.extend(lights)
    net.nodes.append(occupancy_sensor)
    net.nodes.append(light_controller)
    net.nodes.append(motion_sensor)
    net.nodes.append(CO_sensor)
    net.nodes.append(fire_alarm)
    net.nodes.append(smoke_sensor)
    net.nodes.append(humidity_sensor)
    net.nodes.append(ventilator)
    net.nodes.append(CO2_sensor)
    net.nodes.append(heater)
    net.nodes.append(air_conditioner)
    net.nodes.append(thermometer)
    net.nodes.extend(window_sensors)

    # set an attacker computer
    attacker = computer('attacker')
    attacker.setStart()

    # link the attacker with devices
    for node in net.nodes:
        # set the speaker as target
        if node.name == 'air_conditioner':
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
def analyseProbability(net_o, net_p, pri):
    pro_original, _, _ = attackProAnalysis(net_original, pri)
    pro_predicted, _, _ = attackProAnalysis(net_predicted, pri)

    per_err = (abs(pro_original - pro_predicted) / pro_original) * 100

    print('Orignal Probability: %.2f\nPredicted Probability: %.2f\nPercentage Error: %.2f%%\n' % (
        pro_original, pro_predicted, per_err))

# analyse impact of the network using original and predicted vulnerabilities
# net_o: network constructed with original vulnerabilities
# net_p: network constructed with predicted vulnerabilities
# pri: assign a privilege value in construction of lower layer vulnerability connections


def analyseImpact(net_o, net_p, pri):
    impact_original, _, _ = attackImpactAnalysis(net_original, pri)
    impact_predicted, _, _ = attackImpactAnalysis(net_predicted, pri)

    per_err = (abs(impact_original - impact_predicted) / impact_original) * 100

    print('Orignal Impact: %.2f\nPredicted Impact: %.2f\nPercentage Error: %.2f%%\n' % (
        impact_original, impact_predicted, per_err))

# analyse risk of the network using original and predicted vulnerabilities
# net_o: network constructed with original vulnerabilities
# net_p: network constructed with predicted vulnerabilities
# pri: assign a privilege value in construction of lower layer vulnerability connections


def analyseRisk(net_o, net_p, pri):
    risk_original, _, _ = riskAnalysis(net_original, pri)
    risk_predicted, _, _ = riskAnalysis(net_predicted, pri)

    per_err = (abs(risk_original - risk_predicted) / risk_original) * 100

    print('Orignal Risk: %.2f\nPredicted Risk: %.2f\nPercentage Error: %.2f%%\n' % (
        risk_original, risk_predicted, per_err))

# analyse base score of the network using original and predicted vulnerabilities
# net_o: network constructed with original vulnerabilities
# net_p: network constructed with predicted vulnerabilities
# pri: assign a privilege value in construction of lower layer vulnerability connections


def analyseBaseScore(net_o, net_p, pri):
    bs_original, _, _ = baseScoreAnalysis(net_original, pri)
    bs_predicted, _, _ = baseScoreAnalysis(net_predicted, pri)

    per_err = (abs(bs_original - bs_predicted) / bs_original) * 100

    print('Orignal Base Score: %.2f\nPredicted Base Score: %.2f\nPercentage Error: %.2f%%\n' % (
        bs_original, bs_predicted, per_err))


if __name__ == '__main__':

    print('\nAutomated security assessment for interconnected systems')
    print('IoT Graphical Security Model\n')

    # file directories of original and predicted vulnerabiltiies
    dir_o = os.path.join(os.path.dirname(__file__), '../data/original/')
    dir_p = os.path.join(os.path.dirname(__file__), '../data/predicted/')

    # set file names corresponding to each sub-system design
    # file_names = ['Lights.csv','Occupancy sensor.csv','Brightness sensor.csv','Motion sensor.csv']                                                                          # Lighting system
    # file_names = ['Electronic entrance guard.csv','Video surveillance.csv','Burglar alarm.csv','Door window alarm sensor.csv']                                                         # Security system
    # file_names = ['Humidity sensor.csv','Ventilator.csv','CO2 sensor.csv','Heater.csv','Air conditioner.csv','Thermometer.csv','Occupancy sensor.csv','Window sensor.csv']  # HVAC system
    # file_names = ['media player.csv','Screen projector.csv','Smart TV.csv','Speaker.csv','Brightness sensor.csv']                                                                        # Audiovisual system
    # file_names = ['CO sensor.csv','Thermometer.csv','Fire alarm.csv', 'Smoke sensor.csv']                                                                          # Fire Detection system
    # file_names = ['Asset tag.csv','Wearable device.csv','Burglar alarm.csv']                                                                          # Resources Tracking system
    # file_names = ['Electrical current monitoring sensor.csv','Water monitoring sensor.csv','Repair alarm.csv']                                          # Maintenance system
    # file_names = ['Electronic entrance guard.csv','Video surveillance.csv','Burglar alarm.csv','Door window alarm sensor.csv','Asset tag.csv','Wearable device.csv']                                               # Combined Security Tracking system
    file_names = ['media player.csv', 'Screen projector.csv', 'Smart TV.csv', 'Speaker.csv', 'Brightness sensor.csv', 'Lights.csv', 'Occupancy sensor.csv', 'Motion sensor.csv', 'Humidity sensor.csv',
                  'Ventilator.csv', 'CO2 sensor.csv', 'Heater.csv', 'Air conditioner.csv', 'Thermometer.csv', 'Window sensor.csv', 'CO sensor.csv', 'Fire alarm.csv', 'Smoke sensor.csv']         # Combined ALFH system

    # read .csv files and store as a matrix of vulnerabilties
    for file_name in file_names:
        # orignal vulnerabiltiies
        input(os.path.realpath(dir_o + file_name), 1)
        # predicted vulnerabiltiies
        input(os.path.realpath(dir_p + file_name), 2)

    '''
        Sample Networks
    '''

    # create a lighting system network
    # net_original = createLighting(vuls_original)
    # net_predicted = createLighting(vuls_predicted)

    # create a security system network
    # net_original = createSecurity(vuls_original)
    # net_predicted = createSecurity(vuls_predicted)

    # create a HVAC system network
    # net_original = createHVAC(vuls_original)
    # net_predicted = createHVAC(vuls_predicted)

    # create a audiovisual system network
    # net_original = createAudiovisual(vuls_original)
    # net_predicted = createAudiovisual(vuls_predicted)

    # create a fire detection system network
    # net_original = createFireDetection(vuls_original)
    # net_predicted = createFireDetection(vuls_predicted)

    # create a resources tracking system network
    # net_original = createResourcesTracking(vuls_original)
    # net_predicted = createResourcesTracking(vuls_predicted)

    # create a maintenance system network
    # net_original = createMaintenance(vuls_original)
    # net_predicted = createMaintenance(vuls_predicted)

    # create a create a combined security tracking system network
    # net_original = createCombinedSecurityTracking(vuls_original)
    # net_predicted = createCombinedSecurityTracking(vuls_predicted)

    # create a create a combinedALFH system network
    net_original = createCombinedALFH(vuls_original)
    net_predicted = createCombinedALFH(vuls_predicted)

    '''
        Security Metrics
    '''

    # analyse probability of attack
    analyseProbability(net_original,net_predicted,3)

    # analyse impact of attack
    # analyseImpact(net_original,net_predicted,3)

    # analyse risk of attack
    # analyseRisk(net_original,net_predicted,3)

    # analyse CVSS base score
    # analyseBaseScore(net_original, net_predicted, 3)
