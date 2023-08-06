import crcmod.predefined
import codecs
from binascii import unhexlify
from datetime import datetime
import re
import json
import math
import struct


__author__ = "Luis Gonzalez Pincheira"
__copyright__ = "Copyright (c) 2020, Luis Gonzalez Pincheira"
__credits__ = []
__license__ = "BSD-3"
__version__ = "1.0.0-alpha"

class Decode:
    """docstring for Frames"""

    def __init__(self):
        self.PMU_NAMES = []
        self.NUM_PMU = None
        self.TIME_BASE = 1
        self.TYPE_DATA = "AA01"

    def num_pmu(self):
        return self.NUM_PMU

    def phasor_type(self, m):
        return str(codecs.encode(m[0:2], 'hex_codec').upper().decode("utf-8"))

    def check_frame_data(self, m):
        """docstring for FrameData"""
        hex_data = codecs.encode(m, 'hex_codec')
        s = unhexlify(hex_data[:-4])
        a = int(hex_data[-4:], 16)
        crc16 = crcmod.predefined.Crc('ccitt-false')
        crc16.update(s)
        return crc16.crcValue - a

    def data_frame(self, objeto):

        PMU_ARRAY = []
        NUM_PMU = self.NUM_PMU
        PMU_NAME = self.PMU_NAMES
        TIME_BASE = self.TIME_BASE
        SYNC = codecs.encode(objeto[0:2], 'hex_codec').decode("utf-8").upper()
        FRAMESIZE = int(codecs.encode(objeto[2:4], 'hex_codec'), 16)
        IDCODE = int(codecs.encode(objeto[4:6], 'hex_codec'), 16)
        SOC = int(codecs.encode(objeto[6:10], 'hex_codec'), 16)
        FRACSEC = int(codecs.encode(objeto[10:14], 'hex_codec'), 16)
        UNIX_TIMESTAMP = SOC+(float(FRACSEC) / TIME_BASE)
        TIMESTAMP = int((SOC+(float(FRACSEC) / TIME_BASE))*1000)
        x = 14
        for i in range(0, NUM_PMU):
            STAT = codecs.encode(objeto[x:x+2], 'hex_codec').decode("utf-8")
            x += 2
            REAL_PHASOR_1 = 0 if math.isnan(float(struct.unpack(
                '>f', objeto[x:x+4])[0])) else float(struct.unpack('>f', objeto[x:x+4])[0])
            x += 4
            IMG_PHASOR_1 = 0 if math.isnan(float(struct.unpack(
                '>f', objeto[x:x+4])[0])) else float(struct.unpack('>f', objeto[x:x+4])[0])
            x += 4
            REAL_PHASOR_2 = 0 if math.isnan(float(struct.unpack(
                '>f', objeto[x:x+4])[0])) else float(struct.unpack('>f', objeto[x:x+4])[0])
            x += 4
            IMG_PHASOR_2 = 0 if math.isnan(float(struct.unpack(
                '>f', objeto[x:x+4])[0])) else float(struct.unpack('>f', objeto[x:x+4])[0])
            x += 4
            REAL_PHASOR_3 = 0 if math.isnan(float(struct.unpack(
                '>f', objeto[x:x+4])[0])) else float(struct.unpack('>f', objeto[x:x+4])[0])
            x += 4
            IMG_PHASOR_3 = 0 if math.isnan(float(struct.unpack(
                '>f', objeto[x:x+4])[0])) else float(struct.unpack('>f', objeto[x:x+4])[0])
            x += 4
            AFREQ = (float(struct.unpack('>f', objeto[x:x+4])[0])/1000)
            x += 4
            FREQ = 0 if (AFREQ == 0) else (AFREQ + 50)
            DFREQ = float(struct.unpack('>f', objeto[x:x+4])[0])
            x += 4
            dataPhasor = {
                "idConfig": "",
                "pmu": PMU_NAME[i],
                "sync": SYNC,
                "frameSize": FRAMESIZE,
                "idCode": IDCODE,
                "soc": SOC,
                "fracsec": FRACSEC,
                "datetime": None,
                "unixTimestamp":UNIX_TIMESTAMP,
                "stat": STAT,
                "dataPhasor": {"realV1": REAL_PHASOR_1, "imgV1": IMG_PHASOR_1, "realV2": REAL_PHASOR_2, "imgV2": IMG_PHASOR_2, "realV3": REAL_PHASOR_3, "imgV3": IMG_PHASOR_3, "freq": FREQ, "dfreq": DFREQ}
            }
            PMU_ARRAY.append(dataPhasor)
            pass
        # return json.dumps(PMU_ARRAY,indent=4, default=json_util.default)
        return json.dumps(PMU_ARRAY, indent=4)

    def config_frame(self, objeto):
        x = 20
        SYNC = codecs.encode(objeto[0:2], 'hex_codec').upper().decode("utf-8")
        FRAMESIZE = int(codecs.encode(objeto[2:4], 'hex_codec'), 16)
        IDCODE = int(codecs.encode(objeto[4:6], 'hex_codec'), 16)
        SOC = int(codecs.encode(objeto[6:10], 'hex_codec'), 16)
        FRACSEC = int(codecs.encode(objeto[10:14], 'hex_codec'), 16)
        self.TIME_BASE = int(codecs.encode(objeto[14:18], 'hex_codec'), 16)
        TIME = datetime.fromtimestamp(
            SOC+(float(FRACSEC) / self.TIME_BASE)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        self.NUM_PMU = int(codecs.encode(objeto[18:20], 'hex_codec'), 16)
        PMU_DATA = []
        for y in range(0, self.NUM_PMU):
            PMU_NAME = re.sub("\s", '', objeto[x:x+16].decode("utf8"))
            self.PMU_NAMES.append(PMU_NAME)
            x += 16
            IDCODE = int(codecs.encode(objeto[x:x+2], 'hex_codec'), 16)
            x += 2
            FORMAT = str(codecs.encode(objeto[x:x+2], 'hex_codec').upper())
            x += 2
            PHNMR1 = int(codecs.encode(objeto[x:x+2], 'hex_codec'), 16)
            x += 2
            ANNMR1 = int(codecs.encode(objeto[x:x+2], 'hex_codec'), 16)
            x += 2
            DGNMR1 = int(codecs.encode(objeto[x:x+2], 'hex_codec'), 16)
            x += 2
            CHNAM1 = re.sub("\s", '', objeto[x:x+16].decode("utf8"))
            x += 16
            CHNAM2 = re.sub("\s", '', objeto[x:x+16].decode("utf8"))
            x += 16
            CHNAM3 = re.sub("\s", '', objeto[x:x+16].decode("utf8"))
            x += 16
            PHUNIT1 = int(codecs.encode(objeto[x:x+4], 'hex_codec'), 16)
            x += 4
            PHUNIT2 = int(codecs.encode(objeto[x:x+4], 'hex_codec'), 16)
            x += 4
            PHUNIT3 = int(codecs.encode(objeto[x:x+4], 'hex_codec'), 16)
            x += 4
            FNOM = 60 if (
                int(codecs.encode(objeto[x:x+2], 'hex_codec'), 16)) == 0 else 50
            x += 2
            CFGCNT = int(codecs.encode(objeto[x:x+2], 'hex_codec'), 16)
            x += 2
            dataPhasors= {
                "PMU_NAME": PMU_NAME,
                "IDCODE": IDCODE,
                "FORMAT": FORMAT,
                "PHNMR1": PHNMR1,
                "ANNMR1": ANNMR1,
                "DGNMR1": DGNMR1,
                "CHNAM1": CHNAM1,
                "CHNAM2": CHNAM2,
                "CHNAM3": CHNAM3,
                "PHUNIT1": PHUNIT1,
                "PHUNIT2": PHUNIT2,
                "PHUNIT3": PHUNIT3,
                "FNOM": FNOM,
                "CFGCNT": CFGCNT,
            }
            PMU_DATA.append(dataPhasors)
            pass

        config_data = {
            "SYNC": SYNC,
            "IDCODE": IDCODE,
            "SOC": SOC,
            "FRACSEC": FRACSEC,
            "TIME_BASE": self.TIME_BASE,
            "TIME": TIME,
            "NUM_PMU": self.NUM_PMU,
            "PMU_DATA": PMU_DATA
        }
        PMU_DATA = []
        # return  json.dumps(config_data,indent=4, default=json_util.default)
        return json.dumps(config_data, indent=4)