'''
eeboard V 0.1

Coded By Youngsik Kim @ CSEE.HGU
2018. 12.01

Testing Device is connected

print device SN when sucess
'''


from eeboard import Device

import time

dv=Device()
dv.get_device_info()
dv.print_device_info()
dv.open_device()
dv.CloseAll()
