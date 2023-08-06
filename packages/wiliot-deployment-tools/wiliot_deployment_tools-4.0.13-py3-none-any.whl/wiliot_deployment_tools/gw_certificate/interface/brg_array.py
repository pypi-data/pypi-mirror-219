from wiliot_deployment_tools.gw_certificate.interface.pkt_generator import PktGenerator

class BrgArray:
    def __init__(self, num_brgs=3):
        assert num_brgs > 1, 'BrgArray cannot be smaller than 1!'
        self.brg_list = [PktGenerator() for brg in range(num_brgs)]
        self.primary_brg = self.brg_list[0]
        self.secondary_brgs = self.brg_list[1:]
    
    def get_new_pkt_pairs(self) -> list:
        pkts = []
        new_pkt_primary = self.primary_brg.get_new_packet_pair()
        pkts.append(new_pkt_primary)
        for brg in self.secondary_brgs:
            brg.generate_si_from_pkt_id(self.primary_brg.pkt_id_int)
            brg.randomize_rssi_nfpkt()
            brg.data_packet = new_pkt_primary['data_packet']
            pkts.append(brg.get_existing_packet_pair())
        return pkts