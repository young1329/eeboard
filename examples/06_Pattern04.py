'''
eeboard V 0.1

Test for Pattern / Digital IO / Power

Digital Output D22 and D21 set as output and
assgin D22=High, D21=Low

Pattern : 1kHz pulse clock with 50%duty through D23

Coded by Younsik Kim
2018. 09. 15

'''
from eeboard import Power
from eeboard import Pattern
import time
from eeboard import DigitalIO

pwr = Power()
dio = DigitalIO()
pttn=Pattern()

pttn.get_device_info()
pttn.print_device_info()
pttn.open_device()

pttn.DO_reset()

#default 100MHz clock
pttn.DO_check_internal_clock()  #internal clock check


pttn.DO_set_divider(23,500000)
pttn.DO_enable_disable(23,True)
pttn.DO_set_counter(23,1,1)
pttn.DO_set_form(23,'PP')
    
#2. Now let them go out
pttn.DO_start_stop(True) # make them output


dio.SetOutputPins(0x00600000)
dio.SetOutputValues(0x00400000)
dio.GetDigitalIOInputs()


pwr.set_channel_voltage('VP+',5)
pwr.set_channel_current('VP+',500e-3)
pwr.enable_channel('VP+')
pwr.analogIO_ON()

time.sleep(1)
pwr.measure_vmtr()
pwr.analogIO_OFF()
print('Vmtr1=%.2f V\n'%(pwr.get_vmtr(0)))
print('Vmtr2=%.2f V\n'%(pwr.get_vmtr(1)))
print('Vmtr3=%.2f V\n'%(pwr.get_vmtr(2)))
print('Vmtr4=%.2f V\n'%(pwr.get_vmtr(3)))


pttn.CloseAll()

del pttn, pwr, dio
