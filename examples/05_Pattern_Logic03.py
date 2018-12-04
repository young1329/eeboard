'''
eeboard V 0.1

Test Logic / Pattern 02 : Add trigger condition

Pattern out D3-D0 : 4bit counter

Logic : measure 8-bit 1000 samples "Single Acquisition Mode"

Codedy by Yougnsik Kim @ CSEE . HGU
2018. 09.15

'''
from eeboard import Logic
from eeboard import Pattern
import matplotlib.pyplot as plt
import numpy as np


#0. create lg and pt objects
lg = Logic()
pttn = Pattern()

#1. open device
lg.get_device_info()
lg.print_device_info()
lg.open_device()


#2. setup pattern D3-D0 4-bit counter
pttn.DO_reset()
pttn.DO_check_internal_clock()  #internal clock check
pttn.DO_trigsrc('pc')

for i in range(0,4):  #i= 0,1,2,3
    pttn.DO_set_divider(i,1<<i)  #dividing factor 1,2,4,8
    pttn.DO_enable_disable(i,True)
    pttn.DO_set_counter(i,500,500)
    pttn.DO_set_form(i,'PP')
    
pttn.DO_start_stop(True) # make them output


#3. Measure DIO3-DIO0 with 100MHz
lg.DI_reset()
#lg.DI_set_acquisition_mode('Single')
lg.DI_get_internal_clock()
lg.DI_set_acquisition_mode('Record')

lg.DI_set_divider(500)    #divider factor

lg.DI_set_sample_bits(8) #format:among 8, 16, 32
lg.cSamples=5000
lg.DI_set_samples(5000) #

lg.DI_trigsrc('detectdigital')
lg.DI_trig_position(lg.cSamples)
lg.DI_trig_set(1,'fsRise')


#4.0 Excution
pttn.PCtrig()
lg.DI_start_acquisition()
lg.DI_read_record()

lg.CloseAll()
pttn.CloseAll()

# post processing
data = np.zeros(len(lg.rgwSamples))


for idx in range(len(data)):
    data[idx] = lg.rgwSamples[idx] & 0x0F

del lg, pttn

plt.stem(data[0:32],'-.')
plt.show()
