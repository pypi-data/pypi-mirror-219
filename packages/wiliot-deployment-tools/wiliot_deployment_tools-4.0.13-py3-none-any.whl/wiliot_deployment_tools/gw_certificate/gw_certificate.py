import time
import os
from wiliot_deployment_tools.api.extended_api import ExtendedEdgeClient
from wiliot_deployment_tools.common.analysis_data_bricks import initialize_logger
from wiliot_core.utils.utils import WiliotDir
from wiliot_deployment_tools.gw_certificate.interface.ble_simulator import BLESimulator
from wiliot_deployment_tools.gw_certificate.interface.mqtt import MqttClient
from wiliot_deployment_tools.gw_certificate.tests.coupling import CouplingTest
from wiliot_deployment_tools.interface.uart_ports import get_uart_ports

class GWCertificateError(Exception):
    pass

class GWCertificate:
    def __init__(self, gw_id, api_key, owner_id, env):
        self.env_dirs = WiliotDir()
        self.certificate_dir = os.path.join(self.env_dirs.get_wiliot_root_app_dir(), 'gw-certificate')
        self.env_dirs.create_dir(self.certificate_dir)
        self.logger_filename = initialize_logger(self.certificate_dir)

        self.gw_id = gw_id
        self.owner_id = owner_id
        self.edge = ExtendedEdgeClient(api_key, owner_id, env=env)
        self.mqttc = MqttClient(gw_id, owner_id)
        self.uart_comports = get_uart_ports()
        if len(self.uart_comports) < 2: 
            raise GWCertificateError('2 Developments boards need to be connected to USB!')
        self.ble_sim = BLESimulator(self.uart_comports[0])
        # self.sniffer = SnifferClass(self.uart_comports[1])
        self.tests = [CouplingTest(**self.__dict__)]
    
    def run_tests(self):
        for test in self.tests:
            test.run()
"""
Multiple Tags test:
Duplication 1->10
    Per Duplication: 15 -> 255, 30 ms jumps:
        Bridges 1->5
            Randomize start time 0 -> jumps * range (1-5 brgs):
                each bridge echoes a new packet ID
                run 100 times, each time randomize which packets to drop (never drop all of each bridge's si or all data)

IN THE MEANWHILE:
every 30 second: HB
every 1 minute: brg CFG

Uncoupling test:
same as coupling, with GW configured to uncoupled mode.
"""
# TODO - 3 BRG instead of 5
# TODO - Test coupling window
# TODO - NFPKT / RSSI Check all available values: 
# TODO RSSI - 0->127 10 first,/10 last
# TODO NFPKT - 0 ->65535 10 first, /10 last
# TODO Payload incremental
# TODO Reboot
