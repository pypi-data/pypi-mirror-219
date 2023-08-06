import binascii
import datetime
import pandas as pd
import os

import pkg_resources
from wiliot_deployment_tools.ag.ut_defines import BRIDGE_ID, NFPKT, PAYLOAD, RSSI, TIMESTAMP

from wiliot_deployment_tools.ag.wlt_types import GenericV7, WltPkt
from wiliot_deployment_tools.ag.wlt_types_ag import GROUP_ID_SIDE_INFO, Hdr, SideInfo
from wiliot_deployment_tools.ag.wlt_types_data import DataPacket
from wiliot_deployment_tools.common.debug import debug_print

EMPTY_PKT = '000000000000000000000000000000000000000000000000'
class PktGenerator:
    def __init__(self):
        self.bridge_id = 'FFFFFFFFFFFF'
        self.adva = 'FFFFFFFFFFFF'
        self.generate_random_bridge_id()
        
        # Data packet init
        self.data_packet = DataPacket()
        self.pkt_id_int = self.data_packet.generic.pkt_id
        self.pkt_id_bytes = self.pkt_id_int.to_bytes(4, 'big').hex()
            # (int.from_bytes(binascii.unhexlify(self.pkt_id), 'big') +1)        
        # SI packet init
        self.si_packet = self.generate_si_from_pkt_id(self.pkt_id_int)
        self.rssi = self.si_packet.generic.rssi
        self.nfpkt = self.si_packet.generic.nfpkt
                
    def generate_si_from_pkt_id(self, pkt_id_int):
        self.si_packet = WltPkt(hdr=Hdr(group_id=GROUP_ID_SIDE_INFO), generic=SideInfo(brg_mac=int.from_bytes(binascii.unhexlify(self.bridge_id), 'big'), pkt_id=pkt_id_int))
        return self.si_packet
    
    def generate_random_bridge_id(self):
        self.bridge_id = os.urandom(6).hex().upper()
        
    def increment_pkt_id(self):
        self.pkt_id_int = self.pkt_id_int + 1
        self.pkt_id_bytes = self.pkt_id_int.to_bytes(4, 'big').hex()
        self.data_packet.generic.pkt_id = self.pkt_id_int
        self.si_packet.generic.pkt_id = self.pkt_id_int
    
    def randomize_data_packet(self):
        # randomize packet ID
        self.pkt_id_int = int.from_bytes(os.urandom(4), 'big')
        self.pkt_id_bytes = self.pkt_id_int.to_bytes(4, 'big').hex()
        self.data_packet.generic.pkt_id = self.pkt_id_int
        self.si_packet.generic.pkt_id = self.pkt_id_int
        # randomize packet payload
        self.data_packet.generic.payload = int.from_bytes(os.urandom(20), 'big')
        
    def randomize_rssi_nfpkt(self):
        self.rssi = int.from_bytes(os.urandom(1), 'big')
        self.nfpkt = int.from_bytes(os.urandom(2), 'big')
        self.si_packet.generic.rssi = self.rssi
        self.si_packet.generic.nfpkt = self.nfpkt
        return self.rssi, self.nfpkt
    
    def get_existing_packet_pair(self) -> dict:
        return {'data_packet': self.data_packet, 'si_packet': self.si_packet}
    
    def get_new_packet_pair(self) -> dict: 
        #self.randomize_pkt_id()
        self.randomize_data_packet()
        self.randomize_rssi_nfpkt()
        return self.get_existing_packet_pair()
        
    def get_expected_mqtt(self):
        """generates expected MQTT packet"""
        timestamp = int(datetime.datetime.now().timestamp()*1000)
        expected = {TIMESTAMP: timestamp, BRIDGE_ID: self.bridge_id, NFPKT: self.nfpkt, RSSI: self.rssi, PAYLOAD: self.data_packet.dump()[4:]}
        return expected

