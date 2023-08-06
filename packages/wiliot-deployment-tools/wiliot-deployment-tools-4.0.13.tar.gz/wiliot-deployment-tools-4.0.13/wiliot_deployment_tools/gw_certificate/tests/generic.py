import pandas as pd
import tabulate
from wiliot_deployment_tools.api.extended_api import ExtendedEdgeClient
from wiliot_deployment_tools.gw_certificate.interface.ble_simulator import BLESimulator
from wiliot_deployment_tools.gw_certificate.interface.mqtt import MqttClient

PASS_STATUS = {True: 'PASS', False: 'FAIL'}

class GenericTest:
    def __init__(self, mqttc: MqttClient, ble_sim: BLESimulator, edge: ExtendedEdgeClient, gw_id, owner_id, **kwargs):
        self.mqttc = mqttc
        self.ble_sim = ble_sim
        self.edge = edge
        self.report = ''
        self.test_pass = False
    
    def add_to_test_report(self, report):
        self.report += '\n' + report