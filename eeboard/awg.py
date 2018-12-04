''' 
EEBoard control based on Python
Coded by Youngsik Kim @Handong University
Updated to V06 @2018.09.12
	adding destruction
	The object should be del at the end to clear out the device handler
'''
from device import *


awg_channels ={'AWG1':0, 'AWG2':1, 'VP+':2, 'VP-':3}
class AWG(Device):

    def __init__(self,idx=0):
        self.idx = idx;
        Device.__init__(self,idx)
        
    ##########
    #2.0 AWG Control  channel= AWG1:0, AWG2:1, VP+:2, VP-:3
    #                 nodes = Carrier: 0, FM:1, AM:2
    ##########

    def AWG_wform(self,ch,wf):
        wform = {'dc':c_byte(0),'sin':c_byte(1),'square':c_byte(2),'triangle':c_byte(3),'ramp_up':c_byte(4), 'ramp_down':c_byte(5)}
        try:            
            Eflag=dwf.FDwfAnalogOutNodeFunctionSet(self.hdwf[self.idx],awg_channels[ch],c_int(0),wform[wf])
            #print "waveform : %s, %s\n"%(wf,wform[wf])
            if (not Eflag):
                raise ErrMsg("Failed AWG1 Function setup")
        except ErrMsg as emsg:
            print emsg

    def AWG_freq(self,ch,freq):
        try:
            Eflag = dwf.FDwfAnalogOutNodeFrequencySet(self.hdwf[self.idx],awg_channels[ch],c_int(0),c_double(freq))
            #print "signal freq = %f\n"%(freq)
            if (not Eflag):
                raise ErrMsg("Failed AWG1 freq setup")
        except ErrMsg as emsg:
            print emsg
            

    def AWG_amp_offset(self,ch,amp,offset):
        try:
            Eflag = dwf.FDwfAnalogOutNodeAmplitudeSet(self.hdwf[self.idx],awg_channels[ch],c_int(0),c_double(amp))
            Eflag = Eflag and dwf.FDwfAnalogOutNodeOffsetSet(self.hdwf[self.idx],awg_channels[ch],c_int(0),c_double(offset))
            #print "amp=%f, offset =%f\n"%(amp,offset)
            if (not Eflag):
                raise ErrMsg("Failed AWG1 amplitude and offset setup")
        except ErrMsg as emsg:
            print emsg

    def AWG_trig(self,ch,ts):  # ts is in ['none','pc','detectanalog','detectditigal','analogin','digitalin'
        trigsrc = {'none':c_byte(0),'pc':c_byte(1),'detectanalog':c_byte(2),'detectdigital':c_byte(3),'analogin':c_byte(4),'digitalin':c_byte(5)}
        try:
            Eflag = dwf.FDwfAnalogOutTriggerSourceSet(self.hdwf[self.idx],awg_channels[ch],trigsrc[ts])
            #print "AWG trig %s: %s"%(ts,str(trigsrc[ts]))
            if (not Eflag):
                raise ErrMsg("Failed AWG1 trigger source setup")
        except ErrMsg as emsg:
            print emsg
            
    def AWG_enable(self,ch):
        try:
            Eflag = dwf.FDwfAnalogOutNodeEnableSet(self.hdwf[self.idx],awg_channels[ch],c_int(0),True)
            #print "channel %d is enabled\n"%ch
            if (not Eflag):
                raise ErrMsg("Failed AWG1 enable")
        except ErrMsg as emsg:
            print emsg

    def AWG_configure(self,ch):
        try:
            Eflag = dwf.FDwfAnalogOutConfigure(self.hdwf[self.idx],awg_channels[ch],True)
            #print "channel %d is enabled\n"%ch
            if (not Eflag):
                raise ErrMsg("Failed AWG1 enable")
        except ErrMsg as emsg:
            print emsg
            
    def AWG_pctrig(self):
        try:
            Eflag = dwf.FDwfDeviceTriggerPC(self.hdwf[self.idx])
            #print "pc triggered\n"
            if (not Eflag):
                raise ErrMsg("PC trigger error\n")
        except ErrMsg as emsg:
            print emsg
        time.sleep(1)


    # AWG Channel 3 & 4 for power driving
    def AWG_VPsetcurrent(self,ch,crnt):
        try:
            Eflag = dwf.FDwfAnalogOutLimitationSet(self.hdwf[self.idx],awg_channels[ch],c_double(crnt))
            if (not Eflag):
                raise ErrMsg("AWG VP current set error\n")
        except ErrMsg as emsg:
            print emsg

    def AWG_VPsetmode(self,ch,mode): # mode =0 for voltage mode =  1 for current
        try:
            Eflag = dwf.FDwfAnalogOutModeSet(self.hdwf[self.idx],awg_channels[ch],c_int(mode))
            if (not Eflag):
                raise ErrMsg("AWG VP mode set error\n")
        except ErrMsg as emsg:
            print emsg