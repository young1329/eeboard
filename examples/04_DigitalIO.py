'''
eeboard V 0.2
Test for Digital IO

Digital Static IO Test
  Set the pin map : D15-D8 input / D7-D0 output
  Ouput 0x12=0001 0010     D1 and D4 are one and the others are 0
  Connect Vmtr1 -> D0, Vmtr2 -> D1, Vmtr3-> D4, Vmtr4 -> Vcc
  Measure the output voltage with pwr voltage meter

'''

from ..eeboard import DigitalIO
from ..eeboard import Power
import time
# Static Digial IO test Tutorial
pwr = Power()

#1.0 Digital IO Test : connect D4 to D8
dio = DigitalIO()
dio.get_device_info()
dio.open_device()

# reset
dio.Reset_DIO()

# D7-D0 as output D15-D8 as input
dio.SetOutputPins(0x00FF)

#D7:D0 = 0x12 measn D4=1, D1=1 and others are 0
dio.SetOutputValues(0x12)
dio.GetDigitalIOInputs()

#check the dio.InputValues.value = 274L=0x0112
# connect Vmtr3->DO4 and Vmtr4->DO2
time.sleep(1)
pwr.measure_vmtr()
print('Vmtr1=%.2f V\n'%(pwr.get_vmtr(0)))
print('Vmtr2=%.2f V\n'%(pwr.get_vmtr(1)))
print('Vmtr3=%.2f V\n'%(pwr.get_vmtr(2)))
print('Vmtr3=%.2f V\n'%(pwr.get_vmtr(3)))

print(dio.InputValues)


dio.CloseAll()

del dio,pwr
