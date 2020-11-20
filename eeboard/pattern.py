''' 
EEBoard control based on Python
Coded by Youngsik Kim @Handong University
Updated to V0.7 @2020.11.17
	adding destruction
	The object should be del at the end to clear out the device handler
'''

from device import *


class Pattern(Device):
    def __init__(self,idx=0):
        self.idx = idx
        Device.__init__(self,idx)
        self.hzSys = c_double()
    
    def DO_reset(self):
        try:
            Eflag = dwf.FDwfDigitalOutReset(self.hdwf[self.idx])
            if (not Eflag):
                raise ErrMsg("\n Pattern Reset Error\n")
        except ErrMsg as emsg:
            print(emsg)
    
    def DO_check_internal_clock(self):
        try:
            Eflag = dwf.FDwfDigitalOutInternalClockInfo(self.hdwf[self.idx],byref(self.hzSys))
            if (not Eflag):
                raise ErrMsg("\n Fail to read internal clock information \n")
        except ErrMsg as emsg:
            print(emsg)
    
                            # channel int,  fEnable 0 or 1 (true or false )
    def DO_enable_disable(self,channel,fEnable):
        try:
            Eflag = dwf.FDwfDigitalOutEnableSet(self.hdwf[self.idx],c_int(channel),c_uint(fEnable))
            if (not Eflag):
                raise ErrMsg("\n Set output eanble failed\n")
        except ErrMsg as emsg:
            print(emsg)
            
            
    #set tht initial counter value fHigh=1 high, fHigh=0 low and initial divider factor Div
    def DO_set_initial(self,channel,fHigh,Div):
        try:
            Eflag = dwf.FDwfDigitalOutCounterInitSet(self.hdwf[self.idx],c_int(channel),c_uint(fHigh),c_int(Div))
            if(not Eflag):
                raise ErrMsg("\nSet Counter Init Failed\n")
        except ErrMsg as emsg:
            print(emsg)
    
    #similar to set duty but you can assign dividing factor for low and high directly
    def DO_set_counter(self,ch,fLow,fHigh):
        try:                                               
            Eflag = dwf.FDwfDigitalOutCounterSet( \
                self.hdwf[self.idx],c_int(ch),\
                c_uint(fLow),c_uint(fHigh))  #low and high counter
            if (not Eflag):
                raise ErrMsg("\n Duty set error in Digital Out\n")
        except ErrMsg as emsg:
            print(emsg)
    
            
    def DO_set_duty(self,ch,duty):
        try:                                               
            Eflag = dwf.FDwfDigitalOutCounterSet( \
                self.hdwf[self.idx],c_int(ch),\
                c_uint((100-duty)/10),c_uint(duty/10))  #low and high counter
            if (not Eflag):
                raise ErrMsg("\n Duty set error in Digital Out\n")
        except ErrMsg as emsg:
            print(emsg)
                
    # fStart=1 means start, fStart=0 make it stop
    def DO_start_stop(self,fStart):
        try:
            Eflag=dwf.FDwfDigitalOutConfigure(self.hdwf[self.idx],c_int(fStart))
            if (not Eflag):
                raise ErrMsg("\n Counter start/stop failed\n")
        except ErrMsg as emsg:
            print(emsg)
 
    
    def DO_trigsrc(self,ts):   # default is none
        trigsrc = {'none':c_byte(0),'pc':c_byte(1),'detectanalog':c_byte(2),'detectdigital':c_byte(3),'analogin':c_byte(4),'digitalin':c_byte(5),'ext1':c_byte(11)}
        try:
            Eflag = dwf.FDwfDigitalOutTriggerSourceSet(self.hdwf[self.idx],trigsrc[ts])
            if (not Eflag):
                raise ErrMsg("\n Trigger source error in Digital Out\n")
        except ErrMsg as emsg:
            print(emsg)


    # divider value for the specified channel
    def DO_set_divider(self,ch,div): # Freq = 100MHz/div / 10 ( by duty factor 10 )
        try:
            Eflag = dwf.FDwfDigitalOutDividerSet(self.hdwf[self.idx],c_int(ch),c_int(div))
            if (not Eflag):
                raise ErrMsg("\n Divider error in Digital Out\n")
        except ErrMsg as emsg:
            print(emsg)

            
    def PCtrig(self):
        try:
            Eflag = dwf.FDwfDeviceTriggerPC(self.hdwf[self.idx])
            if (not Eflag):
                raise ErrMsg("Failed to pc trigger in sceop\n")
        except ErrMsg as emsg:
            print(emsg)
        time.sleep(1)
        
    def DO_set_form(self,ch, sForm):
        outform={'PP':c_byte(0),'OD':c_byte(1),'OS':c_byte(2),'TS':c_byte(3)}
        try:
            Eflag=dwf.FDwfDigitalOutTypeSet(self.hdwf[self.idx], c_int(ch), outform[sForm])
            if (not Eflag):
                raise ErrMsg("\n Output type setting failed \n")
        except ErrMsg as emsg:
            print(emsg)

    def DO_set_type(self,ch, strType):
        outtype={'Pulse':c_byte(0),'Custom':c_byte(1),'Random':c_byte(2)}
        try:
            Eflag=dwf.FDwfDigitalOutTypeSet(self.hdwf[self.idx], c_int(ch), outtype[strType])
            if (not Eflag):
                raise ErrMsg("\n Output type setting failed \n")
        except ErrMsg as emsg:
            print(emsg)

    def DO_set_data(self,ch,rgBits,count_of_bits):
        try:
            Eflag = dwf.FDwfDigitalOutDataSet(self.hdwf[self.idx],\
                c_int(ch),byref(rgBits),c_int(count_of_bits))
            if (not Eflag):
                ErrMsg("\n DO set data failed \n")
        except ErrMsg as emsg:
            print(emsg)