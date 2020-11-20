''' 
EEBoard control based on Python
Coded by Youngsik Kim @Handong University
Updated to V0.7 @2020.11.17
	adding destruction
	The object should be del at the end to clear out the device handler
'''

from device import *


schannels={'SCOPE1':0, 'SCOPE2':1, 'SCOPE3':2, 'SCOPE4':3}
class Scope(Device):

    def __init__(self,idx=0):
        self.idx = idx;
        Device.__init__(self,idx)
        # Scope
        self.num_of_samples = c_int(1024)
        self.sampling_freq = c_double(100e3) # default sampling frequency
        self.Ch1Voltages = (c_double * self.num_of_samples.value)(0.0)
        self.Ch2Voltages = (c_double * self.num_of_samples.value)(0.0)
        self.Ch3Voltages = (c_double * self.num_of_samples.value)(0.0)
        self.Ch4Voltages = (c_double * self.num_of_samples.value)(0.0)
        
    ###########
    # 3.0 Scope Setup
    ##############
    def SCOPE_init(self):
        try:                        
            Eflag = dwf.FDwfAnalogInFrequencySet(self.hdwf[self.idx],self.sampling_freq)
            Eflag = Eflag and dwf.FDwfAnalogInBufferSizeSet(self.hdwf[self.idx],self.num_of_samples)
            
            Eflag = Eflag and dwf.FDwfAnalogInTriggerSourceSet(self.hdwf[self.idx],c_ubyte(2)) # default detect analog in trigsrcDetectorAnalogIn
            Eflag = Eflag and dwf.FDwfAnalogInTriggerTypeSet(self.hdwf[self.idx],c_int(0)) # default edge by 0 trigtypeEdge
            Eflag = Eflag and dwf.FDwfAnalogInTriggerChannelSet(self.hdwf[self.idx],schannels['SCOPE1']) # default trig is scope 1
            Eflag = Eflag and dwf.FDwfAnalogInTriggerLevelSet(self.hdwf[self.idx],c_double(1.0)) # trigger level 0.0
            Eflag = Eflag and dwf.FDwfAnalogInTriggerConditionSet(self.hdwf[self.idx],c_int(0)) # default rising edge trigcondRisingPositive
            Eflag = Eflag and dwf.FDwfAnalogInTriggerAutoTimeoutSet(self.hdwf[self.idx],c_double(0)) # Set auto time out 0 ( diable auto trigger )
            if ( not Eflag ):
                raise ErrMsg("Failed SCOPE1 frequency setup")
        except ErrMsg as emsg:
            print(emsg)

    def SCOPE_samplingfreq(self,sfreq):
        try:
            self.sampling_freq = c_double(sfreq)
            Eflag = dwf.FDwfAnalogInFrequencySet(self.hdwf[self.idx],self.sampling_freq)
            if (not Eflag):
                raise ErrMsg("Frailed to set sampling frequency %f"%sfreq)
        except ErrMsg as emsg:
            print(emsg)
            
    def SCOPE_trigsrc(self,ts):
        trigsrc = {'none':c_byte(0),'pc':c_byte(1),'detectoranalogin':c_byte(2),'detectordigitalin':c_byte(3),'analogin':c_byte(4),'digitalin':c_byte(5)}
        try:
            Eflag = dwf.FDwfAnalogInTriggerSourceSet(self.hdwf[self.idx],trigsrc[ts])            
            if (not Eflag):
                raise ErrMsg("Failed to set scope trig source set\n")
        except ErrMsg as emsg:
            print(emsg)
            
    def SCOPE_trigtype(self,ttype):
        trigtype = {'edge':0,'pulse':1,'transition':2}
        try:
            Eflag = dwf.FDwfAnalogInTriggerTypeSet(self.hdwf[self.idx],trigtype[ttype])
            if (not Eflag):
                raise ErrMsg("Failed to set scope trig type set\n")
        except ErrMsg as emsg:
            print(emsg)
        
    def SCOPE_trigchannel(self,ch): # channel in  0,1,2,3
        try:
            Eflag = dwf.FDwfAnalogInTriggerChannelSet(self.hdwf[self.idx],schannels[ch])
            if (not Eflag):
                raise ErrMsg("Faile to set the scoep trigger channel set\n")
        except ErrMsg as emsg:
            print(emsg)

    def SCOPE_triglevel(self,level): # trig level in volt
        try:
            Eflag = dwf.FDwfAnalogInTriggerLevelSet(self.hdwf[self.idx],c_double(level))
            if (not Eflag):
                raise ErrMsg("Faile to set the scoep trigger level set\n")
        except ErrMsg as emsg:
            print(emsg)

    def SCOPE_trigcond(self,cond): #cond in 'rise' or 'fall'
        trigcond = {'rise':0,'fall':1}
        try:
            Eflag = dwf.FDwfAnalogInTriggerConditionSet(self.hdwf[self.idx],trigcond[cond])
            if (not Eflag):
                raise ErrMsg("Faile to set the scoep trigger condition set\n")
        except ErrMsg as emsg:
            print(emsg) 

    def SCOPE_enable(self,ch):
        try:
            Eflag = dwf.FDwfAnalogInChannelEnableSet(self.hdwf[self.idx], schannels[ch], c_bool(True))
            if (not Eflag):
                raise ErrMsg("Failed to enable %s channel in scope\n"%ch)
        except ErrMsg as emsg:
            print(emsg)
            
    def SCOPE_offset(self,ch,offset):
        try:
            Eflag = dwf.FDwfAnalogInChannelOffsetSet(self.hdwf[self.idx], schannels[ch], c_double(0.0))
            if (not Eflag):
                raise ErrMsg("Failed to enable %s channel in scope\n"%ch)
        except ErrMsg as emsg:
            print(emsg)

    def SCOPE_range(self,ch,amp):
        try:
            Eflag = dwf.FDwfAnalogInChannelRangeSet(self.hdwf[self.idx], schannels[ch], c_double(amp))
            if (not Eflag):
                raise ErrMsg("Failed to enable %s channel in scope\n"%ch)
        except ErrMsg as emsg:
            print(emsg)


    def SCOPE_pctrig(self):
        try:
            Eflag = dwf.FDwfDeviceTriggerPC(self.hdwf[self.idx])
            if (not Eflag):
                raise ErrMsg("Failed to pc trigger in sceop\n")
        except ErrMsg as emsg:
            print(emsg)
        time.sleep(1)

    def SCOPE_configure(self):
        try:
            Eflag = dwf.FDwfAnalogInConfigure(self.hdwf[self.idx],True,True)
            if (not Eflag):
                raise ErrMsg("Failed to configure analogin\n")
        except ErrMsg as emsg:
            print(emsg)

    def SCOPE_get_data(self):
        sts = c_byte(0)
        try:            
            while (sts.value != 2 ):
                Eflag = dwf.FDwfAnalogInStatus(self.hdwf[self.idx],True,byref(sts))
                #print "STS ="+str(sts.value)+"\n"
                if (not Eflag):
                    raise ErrMsg("Failed to scope get data\n")
                time.sleep(0.001)
        except ErrMsg as emsg:
            print(emsg)
        try:
            Eflag = dwf.FDwfAnalogInStatusData(self.hdwf[self.idx], schannels['SCOPE1'],self.Ch1Voltages,self.num_of_samples)
            Eflag = Eflag and dwf.FDwfAnalogInStatusData(self.hdwf[self.idx], schannels['SCOPE2'],self.Ch2Voltages,self.num_of_samples)
            Eflag = Eflag and dwf.FDwfAnalogInStatusData(self.hdwf[self.idx], schannels['SCOPE3'],self.Ch3Voltages,self.num_of_samples)
            Eflag = Eflag and dwf.FDwfAnalogInStatusData(self.hdwf[self.idx], schannels['SCOPE4'],self.Ch4Voltages,self.num_of_samples)
            if (not Eflag):
                raise ErrMsg("\n Reading Buffer Error in Scope\n")
        except ErrMsg as emsg:
            print(emsg)
        #print "Finished"
      
    def SCOPE_pctrig(self):
        try:
            Eflag = dwf.FDwfDeviceTriggerPC(self.hdwf[self.idx])
            #print "pc triggered\n"
            if (not Eflag):
                raise ErrMsg("PC trigger error\n")
        except ErrMsg as emsg:
            print(emsg)
        time.sleep(1)    