'''
eeboard V 0.2

Coded By Youngsik Kim @ CSEE.HGU
2020. 11.17

Testing Device is connected

print device SN when sucess
'''

from ..eeboard.device import Device

import time

dv=Device()
dv.open_device()
dv.get_device_info()
dv.print_device_info()
dv.CloseAll()
del dv
