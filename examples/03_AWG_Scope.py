'''
eeboard V 0.1
Coded by Youngsik Kim @ CSEE . HGU

test AWG and scope functions
   Generate 1kHz sin wave and measure it with Scope1
   and plot the waveform

'''

from eeboard import Power
from eeboard import AWG
from eeboard import Scope

import time
import matplotlib.pyplot as plt

pwr=Power()
pwr.get_device_info()
pwr.print_device_info()
pwr.open_device()
pwr.reset_analogIO()

#get the number of channels for AnalogIO
pwr.get_number_of_channels()

# get the number of node for channel 1
pwr.get_nodes_of_channels(1)

# figure out channel 1, and node 2
pwr.what_is_channel_node(1,3)

# Configure VP+=2.5V with 50mA current
pwr.set_channel_voltage('VP+',2.5)
pwr.set_channel_current('VP+',50e-3)

pwr.enable_channel('VP+')
pwr.analogIO_ON()

time.sleep(0.5)

pwr.measure_vmtr()

pwr.analogIO_OFF()

print('Vmtr1=%.2f V'%(pwr.get_vmtr(0)))

########
#AWG and Scope Test
#
# AWG armed and wait trigger
awg = AWG()
print "Created Object awg"
# configure the setup
awg.AWG_wform('AWG1','sin')
awg.AWG_freq('AWG1',1000)
awg.AWG_amp_offset('AWG1',2.0,0.0)  #Ready

awg.AWG_enable('AWG1') # Armed

awg.AWG_trig('AWG1','pc')
awg.AWG_configure('AWG1') #Wait

####
#awg.AWG_pctrig() # Trigger and Running


###
#Configure the scope to measure signal
#
sp = Scope()
sp.SCOPE_init()
# define channel 1 condition
sp.SCOPE_enable('SCOPE1')
sp.SCOPE_offset('SCOPE1',0)
sp.SCOPE_range('SCOPE1',5.0)


sp.SCOPE_pctrig() # Triggering
time.sleep(2)

sp.SCOPE_configure() # Armed

sp.SCOPE_get_data()  # Wait to measure the scope data


Ch1V = sp.Ch1Voltages
print('Finised the measurement. Close device\n')

pwr.CloseAll()

plt.plot(sp.Ch1Voltages)
plt.show()

del pwr,awg,sp
