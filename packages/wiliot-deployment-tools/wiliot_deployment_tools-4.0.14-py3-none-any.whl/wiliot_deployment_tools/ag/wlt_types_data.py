from wiliot_deployment_tools.ag.wlt_types import WltPkt
from wiliot_deployment_tools.ag.ut_defines import *
from wiliot_deployment_tools.ag.wlt_types_ag import *

DATA_DEFAULT_GROUP_ID = 0x020000

class GenericPacket():
    def __init__(self, payload=0, pkt_id=0):
        self.payload = payload
        self.pkt_id = pkt_id

    def __eq__(self, other):
        if isinstance(other, GenericV7):
            return (
                self.payload == other.payload and
                self.pkt_id == other.pkt_id
            )
        return False

    def dump(self):
        string = bitstruct.pack("u160u32", self.payload, self.pkt_id)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u160u32", binascii.unhexlify(string))
        self.payload = d[0]
        self.pkt_id = d[1]


class DataPacket(WltPkt):
    def __init__(self, *args, **kwargs):
        super().__init__(hdr=Hdr(), generic=GenericPacket(), *args, **kwargs)
        self.hdr.group_id = DATA_DEFAULT_GROUP_ID
    
    def set(self, string):
        if not string.startswith("1E16"):
            string = "1E16" + string
        self.hdr.set(string[0:14])
        if self.hdr.group_id == DATA_DEFAULT_GROUP_ID:
            self.generic = GenericPacket()
            self.generic.set(string[14:62])
        else:
            super().set(string)
            
    def dump(self):
        return super().dump()