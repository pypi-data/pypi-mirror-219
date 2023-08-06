from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.gw_certificate.interface.brg_array import BrgArray
from wiliot_deployment_tools.gw_certificate.interface.if_defines import BRIDGES, DUPLICATIONS, TIME_DELAYS
from wiliot_deployment_tools.gw_certificate.interface.packet_error import PacketError
import pkg_resources
import pandas as pd

CSV_NAME = 'packet_table.csv'
PACKET_TABLE_CSV_PATH = pkg_resources.resource_filename(__name__, CSV_NAME)

class GeneratedPacketTable:
    
    def __init__(self) -> None:
        self.brg_array = BrgArray()
        self.table = pd.read_csv(PACKET_TABLE_CSV_PATH)
    
    def get_data(self, duplication, time_delay, bridge_idx) -> list:    
        assert duplication in DUPLICATIONS, 'Invalid Duplication'
        assert time_delay in TIME_DELAYS, 'Invalid Time Delay'
        assert bridge_idx in BRIDGES, 'Invalid Bridge'
        
        t = self.table
        return t.loc[((t['duplication']==duplication) &
                            (t['time_delay'] == time_delay) &
                            (t['bridge_idx'] == bridge_idx))].to_dict('records')[0]
            
    def _generate_packet_table(self):
        packet_list = []
        for duplication in DUPLICATIONS:
            debug_print(f'Duplication {duplication}')
            for time_delay in TIME_DELAYS:
                debug_print(f'Time Delay {time_delay}')

                pkts = self.brg_array.get_new_pkt_pairs()
                for idx, brg in enumerate(self.brg_array.brg_list):
                    debug_print(f'Bridge {idx}')
                    data = pkts[idx]['data_packet'].dump()
                    si = pkts[idx]['si_packet'].dump()
                    packet_error = PacketError()._generate_packet_error(duplication)
                    brg_id = self.brg_array.brg_list[idx].bridge_id
                    # log the sent packet with relevant info from run
                    expected_pkt = brg.get_expected_mqtt()
                    expected_pkt.update({'duplication': duplication, 'time_delay': time_delay,
                                        'packet_error': packet_error, 'si_rawpacket': si, 'data_rawpacket': data})
                    packet_list.append({'duplication': duplication,
                                        'time_delay': time_delay,
                                        'bridge_idx': idx,
                                        'packet_error': packet_error,
                                        'expected_mqtt': expected_pkt
                                        ,'data': data, 'si': si, 'bridge_id': brg_id 
                                        })
        pd.DataFrame(packet_list).to_csv(CSV_NAME)

class CouplingRunData:
    def __init__(self, data) -> None:
        self.duplication = data['duplication']
        self.time_delay = data['time_delay']
        self.bridge_idx = data['bridge_idx']
        self.packet_error = eval(data['packet_error'])
        self.expected_mqtt = eval(data['expected_mqtt'])
        self.data = data['data']
        self.si = data['si']
        self.bridge_id = data['bridge_id']   
                 
    @classmethod
    def get_data(cls, duplication, time_delay, bridge_idx):
        packet_data = GeneratedPacketTable().get_data(duplication, time_delay, bridge_idx)
        return cls(packet_data)

    
if __name__ == "__main__":
    GeneratedPacketTable()._generate_packet_table()   
