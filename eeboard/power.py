''' 
EEBoard control based on Python
Coded by Youngsik Kim @Handong University
Updated to V0.7 @2020.11.17
	adding destruction
	The object should be del at the end to clear out the device handler
'''

from device import *

channels = {'Vcc':0, 'VP+':1, 'VP-':2, 'Vref1':3, 'Vref2':4,
           'Vmtr1':5,'Vmtr2':6, 'Vmtr3':7, 'Vmtr4':8}
nodes = {'Enable':0, 'Voltage':1,'Current':2,'Power':3}

class Power(Device):
    def __init__(self,idx=0):
        self.idx = idx;
        self.nChannel = c_int()
        self.szChannel = create_string_buffer(32)
        self.szLabel = create_string_buffer(16)
        self.szNode = create_string_buffer(32)
        self.szUnits = create_string_buffer(16)
        #Current for power supply
        self.crntVP = c_double()
        self.crntVN = c_double()
        self.crntVCC = c_double()
        
        Device.__init__(self,idx)
        #Vmtr Variables
        self.Vmtr = [c_double(), c_double(), c_double(), c_double()]
        #print ('pwr idx is %d'%self.idx)

    ######   
    #1.0AnalogIO (Vcc:0, VP+:1, VP-:2, Vref1:3, Vref:4, Vmtr1-4:5-8
    #####

    def reset_analogIO(self):
        dwf.FDwfAnalogIOReset(self.hdwf[self.idx])
        dwf.FDwfAnalogIOConfigure(self.hdwf[self.idx])

    def get_number_of_channels(self):
        try:
            Eflag = dwf.FDwfAnalogIOChannelCount(self.hdwf[self.idx],byref(self.nChannel))
            if(not Eflag):
                raise ErrMsg('Cannot get the number of channel')
            else:
                print('Numberof Channel is %d \n'%(self.nChannel.value))
        except ErrMsg as emsg:
            print(emsg)

    def get_nodes_of_channels(self,chnl=0):
        nNode = c_int()
        try:
            Eflag = dwf.FDwfAnalogIOChannelInfo(self.hdwf[self.idx],chnl,byref(nNode))
            Eflag = dwf.FDwfAnalogIOChannelName(self.hdwf[self.idx],chnl,self.szChannel,self.szLabel)
            if (Eflag):
                print('Number of nodes of the channel(%d, %s, %s) is %d \n'%(chnl,
                                                                          self.szChannel.value,
                                                                          self.szLabel.value,
                                                                          nNode.value))
            else:
                raise ErrMsg('Cannot get the infomation %d channel'%(chnl))
        except ErrMsg as emsg:
            self.CloseAll()
            print(emsg)
    def what_is_channel_node(self,chnl=0,node=0):
        try:
            Eflag = dwf.FDwfAnalogIOChannelName(self.hdwf[self.idx],chnl,self.szChannel,self.szLabel)
            Eflag = dwf.FDwfAnalogIOChannelNodeName(self.hdwf[self.idx],chnl,node,
                                                    self.szNode,
                                                    self.szUnits)
            if (Eflag):
                print('Channel(%d): %s, %s\n'%(chnl,self.szChannel.value, self.szLabel.value))
                print('Node(%d) : %s, %s\n'%(node,self.szNode.value,self.szUnits.value))
            else:
                raise ErrMsg('Cannot figure it out %d channel'%(chnl))
        except ErrMsg as emsg:
            self.CloseAll()
            print(emsg)

    
    def enable_channel(self,chnl):
        try:
            if not(chnl in ('Vcc','VP+','VP-','Vref1','Vref2')):
                raise ErrMsg("analog IO : 0(Vcc), 1(VP+), 2(VP-),3(Vref1),4(Vref2")
            Eflag=dwf.FDwfAnalogIOChannelNodeSet(self.hdwf[self.idx],c_int(channels[chnl]),c_int(nodes['Enable']),c_double(True))
            if (not Eflag):
                raise ErrMsg("Channel(%s) cannot be enabled"%chnl)             
        except ErrMsg as emsg:
            print(emsg)

    def disable_channel(self,chnl):
        try:
            if not(chnl in ('Vcc','VP+','VP-','Vref1','Vref2')):
                raise ErrMsg("analog IO : 0(Vcc), 1(VP+), 2(VP-),3(Vref1),4(Vref2")
            Eflag=dwf.FDwfAnalogIOChannelNodeSet(self.hdwf[self.idx],c_int(channels[chnl]),c_int(nodes['Enable']),c_double(False))
            if (not Eflag):
                raise ErrMsg("Channel(%s) cannot be enabled"%chnl)             
        except ErrMsg as emsg:
            print(emsg)
    
    
    def set_channel_voltage(self,chnl,Vltg):
        try:
            if not(chnl in ('Vcc','VP+','VP-','Vref1','Vref2')):
                raise ErrMsg("analog IO : 0(VCC) 1(VP+), 2(VP-),3(Vref1),4(Vref2")
            if (chnl == 'Vcc' and not(Vltg in (3.3, 5.0)) ):
                raise ErrMsg("Vcc can have only 3.3 or 5.0 two values")
            if (chnl == 'VP+' and Vltg <0):
                raise ErrMsg("VP+ should be postive voltage supply%.3f\n"%(Vltg))
            if (chnl == 'VP-' and Vltg >0 ):
                raise ErrMsg("VP- should be negative voltage %.3f\n"%(Vltg))
            Eflag=dwf.FDwfAnalogIOChannelNodeSet(self.hdwf[self.idx],c_int(channels[chnl]),c_int(nodes['Voltage']),c_double(Vltg))
            if (not Eflag):
                raise ErrMsg("Channel(%s) voltage set error"%chnl)    
        except ErrMsg as emsg:
            print(emsg)
    
    def set_channel_current(self,chnl,Crrnt):
        try:
            if not(chnl in ('VP+', 'VP-')):
                raise ErrMsg("analog IO : current can be set on 1(VP+) and 2(VP-)")
            if (chnl == 'VP+' and Crrnt<0):
                raise ErrMsg("VP+ needs positive current level")
            if (chnl == 'VP-' and Crrnt>0):
                raise ErrMsg("VP- needs negative current level")
            Eflag = dwf.FDwfAnalogIOChannelNodeSet(self.hdwf[self.idx],c_int(channels[chnl]),c_int(nodes['Current']),c_double(Crrnt))            
            if (not Eflag):
                raise ErrMsg("Channel(%s) current set error"%chnl)            
        except ErrMsg as emsg:
            print(emsg)
        
    def analogIO_configure(self):
        try:
            Eflag = dwf.FDwfAnalogIOConfigure(self.hdwf[self.idx])
            if (not Eflag):
                raise ErrMsg("Analog IO Configured")
        except ErrMsg as emsg:
            print(emsg)
        
    def analogIO_ON(self):
        try:
            Eflag = dwf.FDwfAnalogIOEnableSet(self.hdwf[self.idx],True)
            if (not Eflag):
                raise ErrMsg("Analog IO cannot be On")
        except ErrMsg as emsg:
            print(emsg)
            
    def analogIO_OFF(self):
        try:
            Eflag = dwf.FDwfAnalogIOEnableSet(self.hdwf[self.idx],False)
            if (not Eflag):
                raise ErrMsg("Anloag IO cannot be OFF")
        except ErrMsg as emsg:
            print(emsg)
        
    
    def measure_vmtr(self):
        try:
            Eflag = dwf.FDwfAnalogIOStatus(self.hdwf[self.idx])
            Eflag = dwf.FDwfAnalogIOStatus(self.hdwf[self.idx])
            Eflag = dwf.FDwfAnalogIOStatus(self.hdwf[self.idx])            
            if (not Eflag):
                raise ErrMsg("Analog IO Channel read error")
            for idx in range(4):
                Eflag = dwf.FDwfAnalogIOChannelNodeStatus(self.hdwf[self.idx],c_int(5+idx),c_int(0),byref(self.Vmtr[idx]))
                
            if (not Eflag):
                raise ErrMsg("Vmtr1 read error")                        
        except ErrMsg as emsg:
            print(emsg)
            
    def get_vmtr(self,idx):
        return self.Vmtr[idx].value;

    def get_crntVP(self):
        try:
            Eflag = dwf.FDwfAnalogIOStatus(self.hdwf[self.idx])
            if (not Eflag):
                raise ErrMsg("AnalogIO Status error")

            Eflag = dwf.FDwfAnalogIOChannelNodeStatus(self.hdwf[self.idx],c_int(1),c_int(2),byref(self.crntVP))
            if (not Eflag):
                raise ErrMsg("get_crntVP error")
            return self.crntVP
        except ErrMsg as emsg:
            print(emsg)

    def get_crntVN(self):
        try:
            Eflag = dwf.FDwfAnalogIOStatus(self.hdwf[self.idx])
            if (not Eflag):
                raise ErrMsg("AnalogIO Status error")

            Eflag = dwf.FDwfAnalogIOChannelNodeStatus(self.hdwf[self.idx],c_int(1),c_int(2),byref(self.crntVN))
            if (not Eflag):
                raise ErrMsg("get_crntVN error")
            return self.crntVN
        except ErrMsg as emsg:
            print(emsg)

    def get_crntVCC(self):
        try:
            Eflag = dwf.FDwfAnalogIOStatus(self.hdwf[self.idx])
            if (not Eflag):
                raise ErrMsg("AnalogIO Status error")

            Eflag = dwf.FDwfAnalogIOChannelNodeStatus(self.hdwf[self.idx],c_int(1),c_int(2),byref(self.crntVCC))
            if (not Eflag):
                raise ErrMsg("get_crntVCC error")
            return self.crntVP
        except ErrMsg as emsg:
            print(emsg)
            
if __name__ == '__main__':

    import time
    
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
    pwr.set_channel_voltage('Vref1',4.0)
    pwr.set_channel_voltage('Vref2',-3.0)
    pwr.set_channel_voltage('VP+',5.0)
    pwr.set_channel_current('VP+',50e-3)
    
    pwr.enable_channel('VP+')
    pwr.enable_channel('Vref1')
    pwr.enable_channel('Vref2')
    pwr.analogIO_ON()
    
    time.sleep(1)
    
    pwr.measure_vmtr()
    
    pwr.analogIO_OFF()
    
    print('Vmtr1=%.2f V\n'%(pwr.get_vmtr(0)))
    print('Vmtr2=%.2f V\n'%(pwr.get_vmtr(1)))
    print('Vmtr3=%.2f V\n'%(pwr.get_vmtr(2)))
    print('Vmtr4=%.2f V'%(pwr.get_vmtr(3)))
    
    del pwr