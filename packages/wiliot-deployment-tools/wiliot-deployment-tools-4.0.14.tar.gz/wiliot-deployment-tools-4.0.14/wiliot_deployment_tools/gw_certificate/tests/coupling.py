import datetime
import time
import pandas as pd
import tabulate
from wiliot_deployment_tools.ag.ut_defines import BRIDGE_ID, NFPKT, PAYLOAD, RSSI, TIMESTAMP
from wiliot_deployment_tools.api.extended_api import ExtendedEdgeClient
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.gw_certificate.interface import packet_error
from wiliot_deployment_tools.gw_certificate.interface.ble_simulator import BLESimulator
from wiliot_deployment_tools.gw_certificate.interface.brg_array import BrgArray
from wiliot_deployment_tools.gw_certificate.interface.if_defines import BRIDGES, DEFAULT_DELAY, DEFAULT_OUTPUT_POWER, DUPLICATIONS, TIME_DELAYS
from wiliot_deployment_tools.gw_certificate.interface.mqtt import MqttClient
from wiliot_deployment_tools.gw_certificate.interface.pkt_generator import PktGenerator
from wiliot_deployment_tools.gw_certificate.tests.generated_packet_table import CouplingRunData
from wiliot_deployment_tools.gw_certificate.tests.generic import PASS_STATUS, GenericTest
from wiliot_deployment_tools.gw_certificate.interface.packet_error import PacketError

RECEIVED = 'received'
SHARED_COLUMNS = [PAYLOAD, BRIDGE_ID, NFPKT, RSSI]
INIT_STAGES_DUPLICATIONS = [i for i in range(3,7)]

# TEST STAGES

class CouplingTestError(Exception):
    pass

class GenericCouplingStage():
    def __init__(self, mqttc:MqttClient, ble_sim:BLESimulator, stage_name, randomize=False, **kwargs):
        #Clients
        self.mqttc = mqttc
        self.ble_sim = ble_sim
        #Stage Params
        self.stage_name = stage_name
        self.randomize = randomize
        self.stage_pass = False
        self.report = ''
        # Packets list
        self.local_pkts = []
        self.mqtt_pkts = []
        # Packet Error / Run data
        self.packet_error = PacketError()
        self.run_data = CouplingRunData
    
    def prepare_stage(self):
        debug_print(f'### Starting Stage: {self.stage_name}')
        self.mqttc.flash_pkts()
        self.ble_sim.set_sim_mode(True)
        
    
    def fetch_mqtt_from_stage(self):
        self.mqtt_pkts = self.mqttc.get_coupled_tags_pkts()

    def compare_local_mqtt(self):
        self.fetch_mqtt_from_stage()
        local_pkts_df = pd.DataFrame(self.local_pkts)
        mqtt_pkts_df = pd.DataFrame(self.mqtt_pkts)
        if not set(SHARED_COLUMNS) <= set(mqtt_pkts_df.columns):
            mqtt_pkts_df[SHARED_COLUMNS] = 0
        comparison = local_pkts_df
        received_pkts_df = pd.merge(local_pkts_df[SHARED_COLUMNS], mqtt_pkts_df[SHARED_COLUMNS], how='inner')
        received_pkts = set(received_pkts_df[PAYLOAD])
        comparison[RECEIVED] = comparison[PAYLOAD].isin(received_pkts)
        self.comparison = comparison
    
    def add_to_stage_report(self, report):
        self.report += '\n' + report
    
    def generate_stage_report(self):
        self.compare_local_mqtt()
        report = []
        num_pkts_sent = len(self.comparison)
        num_pkts_received = self.comparison['received'].eq(True).sum()
        self.stage_pass = num_pkts_sent == num_pkts_received
        report.append((('Number of packets sent'), num_pkts_sent))
        report.append((('Number of packets received'), num_pkts_received))
        self.add_to_stage_report(f'---Stage {self.stage_name} {PASS_STATUS[self.stage_pass]}')
        self.add_to_stage_report(tabulate.tabulate(pd.DataFrame(report), showindex=False))
        self.add_to_stage_report('Packets not received:')
        self.add_to_stage_report(tabulate.tabulate(pd.DataFrame(self.comparison[self.comparison[RECEIVED]==False]), headers='keys', showindex=False))
        debug_print(self.report)
        return self.report
    
class InitStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name='Init Stage')
        self.pkt_gen = PktGenerator()
    
    def run(self):
        for duplication in INIT_STAGES_DUPLICATIONS:
            if self.randomize:
                new_pkt = self.pkt_gen.get_new_packet_pair()
                self.local_pkts.append(self.pkt_gen.get_expected_mqtt())
                data = new_pkt['data_packet'].dump()
                si = new_pkt['si_packet'].dump()
            else:
                run_data = self.run_data.get_data(duplication, DEFAULT_DELAY, BRIDGES[0])
                data = run_data.data
                si = run_data.si
                self.local_pkts.append(run_data.expected_mqtt)
            self.ble_sim.send_data_si_pair(data, si, duplication)
        time.sleep(5)

class OneBrgStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name='One Bridge Stage')
        self.pkt_gen = PktGenerator()
    
    def run(self):
        for duplication in DUPLICATIONS: #tqdm(duplications, desc='Duplications', position=1, leave=True):
            debug_print(f'Duplication {duplication}')
            for time_delay in TIME_DELAYS: #tqdm(time_delays, desc='Time Delays', position=2, leave=True):
                debug_print(f'Time Delay {time_delay}')
                if self.randomize:
                    new_pkt = self.pkt_gen.get_new_packet_pair()
                    self.local_pkts.append(self.pkt_gen.get_expected_mqtt())
                    data = new_pkt['data_packet'].dump()
                    si = new_pkt['si_packet'].dump()
                    expected_pkt = self.pkt_gen.get_expected_mqtt()
                    packet_error = self.packet_error._generate_packet_error(duplication)
                    expected_pkt.update({'duplication': duplication, 'time_delay': time_delay,
                        'packet_error': packet_error, 'si_rawpacket': si, 'data_rawpacket': data})
                else:
                    run_data = self.run_data.get_data(duplication, time_delay, BRIDGES[0])
                    data = run_data.data
                    si = run_data.si
                    packet_error = run_data.packet_error
                    self.local_pkts.append(run_data.expected_mqtt)
                self.ble_sim.send_data_si_pair(data, si, duplication, delay=time_delay, packet_error=packet_error)
        time.sleep(5)

class ThreeBrgInitStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name='Three Bridge Init Stage')
        self.brg_array = BrgArray()
    
    def run(self):
        duplication = DUPLICATIONS[3]
        time_delay = TIME_DELAYS[0]
        if self.randomize:
            # Generate new random packet
            pkts = self.brg_array.get_new_pkt_pairs()
            for idx, brg in enumerate(self.brg_array.brg_list):
                debug_print(f'BRG: {brg.bridge_id}')
                data = pkts[idx]['data_packet'].dump()
                si = pkts[idx]['si_packet'].dump()
                packet_error = self.packet_error._generate_packet_error(duplication)
                # log the sent packet with relevant info from run
                expected_pkt = brg.get_expected_mqtt()
                expected_pkt.update({'duplication': duplication, 'time_delay': time_delay,
                                    'packet_error': packet_error, 'si_rawpacket': si, 'data_rawpacket': data, 'brg_idx': idx})
                self.local_pkts.append(expected_pkt)
                self.ble_sim.send_data_si_pair(data, si, duplicates=duplication, output_power=DEFAULT_OUTPUT_POWER,
                                               delay=time_delay, packet_error=packet_error)
        else:
            for brg_idx in BRIDGES:
                run_data = self.run_data.get_data(duplication, time_delay, brg_idx)
                data = run_data.data
                si = run_data.si
                packet_error = run_data.packet_error
                self.local_pkts.append(run_data.expected_mqtt)
                self.ble_sim.send_data_si_pair(data, si, duplication, delay=time_delay, packet_error=packet_error)
            time.sleep(5)
        


class ThreeBrgStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name='Three Bridge Stage')
        self.brg_array = BrgArray()

    
    def run(self):
        for duplication in DUPLICATIONS:
            debug_print(f'Duplication {duplication}')
            for time_delay in TIME_DELAYS:
                debug_print(f'Time Delay {time_delay}')
                if self.randomize:
                    # Generate new random packet
                    pkts = self.brg_array.get_new_pkt_pairs()
                    for idx, brg in enumerate(self.brg_array.brg_list):
                        debug_print(f'BRG: {brg.bridge_id}')
                        data = pkts[idx]['data_packet'].dump()
                        si = pkts[idx]['si_packet'].dump()
                        packet_error = self.packet_error._generate_packet_error(duplication)
                        # log the sent packet with relevant info from run
                        expected_pkt = brg.get_expected_mqtt()
                        expected_pkt.update({'duplication': duplication, 'time_delay': time_delay,
                                            'packet_error': packet_error, 'si_rawpacket': si, 'data_rawpacket': data, 'brg_idx': idx})
                        self.local_pkts.append(expected_pkt)
                        self.ble_sim.send_data_si_pair(data, si, duplicates=duplication, output_power=DEFAULT_OUTPUT_POWER,
                                                    delay=time_delay, packet_error=packet_error)
                else:
                    for brg_idx in BRIDGES:
                        run_data = self.run_data.get_data(duplication, time_delay, brg_idx)
                        data = run_data.data
                        si = run_data.si
                        packet_error = run_data.packet_error
                        self.local_pkts.append(run_data.expected_mqtt)
                        self.ble_sim.send_data_si_pair(data, si, duplication, delay=time_delay, packet_error=packet_error)
        time.sleep(5)


# TEST CLASS

STAGES = [InitStage, OneBrgStage, ThreeBrgInitStage, ThreeBrgStage]

class CouplingTest(GenericTest):
    def __init__(self, **kwargs):        
        self.__dict__.update(kwargs)
        self.randomize=False
        super().__init__(**self.__dict__)
        self.stages = [stage(**self.__dict__) for stage in STAGES]

    def enter_dev_mode(self):
        self.edge.enter_dev_mode(self.gw_id)
        gw_info = self.mqttc.get_gw_info()
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=3)
        while datetime.datetime.now() < timeout:
            gw_seen = self.mqttc.userdata['gw_seen']
            if gw_seen is True or gw_info is not False:
                debug_print(f'GW {self.gw_id} In DevMode')
                return True
            time.sleep(10)
        raise CouplingTestError('Cannot enter GW DevMode!')
    
    def run(self):
        self.enter_dev_mode()
        self.test_pass = True
        for stage in self.stages:
            stage.prepare_stage()
            stage.run()
            self.add_to_test_report(stage.generate_stage_report())
            if stage.stage_pass == False:
                self.test_pass = False
        debug_print('\n----')
        debug_print(f'Coupling Test {PASS_STATUS[self.test_pass]}')
        debug_print(self.report)
        self.exit_dev_mode()
    
    def exit_dev_mode(self):
        self.mqttc.exit_dev_mode()
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=3)
        while datetime.datetime.now() < timeout:
            online_status = self.edge.check_gw_online([self.gw_id])
            if online_status is not False:
                debug_print(f'GW {self.gw_id} Out Of DevMode')
                return True
            time.sleep(10)
        raise CouplingTestError('Cannot exit GW DevMode!')
