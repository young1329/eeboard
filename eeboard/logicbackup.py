''' 
EEBoard control based on Python
Coded by Youngsik Kim @Handong University
Updated to V06 @2018.09.12
	adding destruction
	The object should be del at the end to clear out the device handler
'''

from .device import *

class Logic(Device): 
    def __init__(self,idx=0):
        self.idx = idx;
        Device.__init__(self,idx)
        self.IntClk=c_double()
        self.cSamples=2000
        self.rgwSamples = (c_uint16*self.cSamples)() 
        self.nBits = 16
        self.nBytes = 2
        

    def DI_reset(self):
        try:
            Eflag=dwf.FDwfDigitalInReset(self.hdwf[self.idx])
            if (not Eflag):
                raise ErrMsg("\n Logic reset error \n")
        except ErrMsg as emsg:
            print emsg
    def DI_set_acquisition_mode(self,aMode):
        acqModes = {'Single':acqmodeSingle, 'ScanShift':acqmodeScanShift,'ScanScreen':acqmodeScanScreen,'Record':acqmodeRecord}
        try:
            Eflag=dwf.FDwfDigitalInAcquisitionModeSet(self.hdwf[self.idx],acqModes[aMode])
            if(not Eflag):
                raise ErrMsg("\n Logic Analyzer Acquisition Mode Set Error \n")
        except ErrMsg as emsg:
            print emsg
            
    def DI_trigsrc(self,ts):
        trigsrc = {'none':c_byte(0),'pc':c_byte(1),'detectanalog':c_byte(2),'detectdigital':c_byte(3),'analogin':c_byte(4),'digitalin':c_byte(5),'ext1':c_byte(11)}
        try:
            Eflag = dwf.FDwfDigitalInTriggerSourceSet(self.hdwf[self.idx],trigsrc[ts])
            if (not Eflag):
                raise ErrMsg("\n Trigger source error in Digital Out\n")
        except ErrMsg as emsg:
            print emsg
            
    def DI_trig_position(self,nPosition):
        try:
            Eflag = dwf.FDwfDigitalInTriggerPositionSet(self.hdwf[self.idx],c_int(nPosition))
            if (not Eflag):
                ErrMsg("\n Fail to set DI trig position set \n")
        except ErrMsg as emsg:
            print emsg

    def DI_trig_prefill(self,nFill):
        try:
            Eflag = dwf.FDwfDigitalInTriggerPrefillSet(self.hdwf[self.idx],c_int(nFill))
            if (not Eflag):
                ErrMsg("\n Fail to set DI trig prefill set \n")
        except ErrMsg as emsg:
            print emsg
            
    # fsTye = [fsLow, fsHigh, fsRise, fsFall 1=D0, 2=D1, 4=D2, 8=D3 ... etc
    def DI_trig_set(self,channel,fsType='fsRise'):
        try:
            if (fsType == 'fsLow' ):
                Eflag=dwf.FDwfDigitalInTriggerSet(self.hdwf[self.idx], c_int(channel), c_int(0), c_int(0), c_int(0))
            elif (fsType=='fsHigh'):
                Eflag = dwf.FDwfDigitalInTriggerSet(self.hdwf[self.idx], c_int(0), c_int(channel), c_int(0), c_int(0))
            elif (fsType=='fsFall') :
                Eflag = dwf.FDwfDigitalInTriggerSet(self.hdwf[self.idx], c_int(0), c_int(0), c_int(0), c_int(channel))
            else:
                Eflag = dwf.FDwfDigitalInTriggerSet(self.hdwf[self.idx], c_int(0), c_int(0), c_int(channel), c_int(0))
            
            if (not Eflag):
                raise ErrMsg("\n faile to DI trig set \n")
        except ErrMsg as emsg:
            print emsg
    
    def DI_get_internal_clock(self):
        try:
            Eflag=dwf.FDwfDigitalInInternalClockInfo(self.hdwf[self.idx],byref(self.IntClk))
            if (not Eflag):
                raise ErrMsg("\n Fail to get the internal clock informatoin \n")
        except ErrMsg as emsg:
            print emsg
 
    def DI_set_divider(self,fDiv):
        try:
            Eflag = dwf.FDwfDigitalInDividerSet(self.hdwf[self.idx],c_int(fDiv))
            if (not Eflag):
                raise ErrMsg("\n Fail to set the clock dividing factor \n")
        except ErrMsg as emsg:
            print emsg
    #set number of sample buffers
    def DI_set_samples(self,num_of_samples):
        self.cSamples = num_of_samples
        if (self.nBits == 8):
            self.rgwSamples = (c_uint8 * self.cSamples)()
        if (self.nBits == 16):
            self.rgwSamples = (c_uint16*self.cSamples)()
        else:
            self.rgwSamples = (c_uint32*self.cSamples)()
            
        try:
            Eflag = dwf.FDwfDigitalInBufferSizeSet(self.hdwf[self.idx], c_int(self.cSamples))
            if (not Eflag):
                raise ErrMsg("\n Error to set the DI sample buffer \n")
        except ErrMsg as emsg:
            print emsg
            
    # set the number of bits : valid = 8, 16, 32
    def DI_set_sample_bits(self,nBits):
        self.nBits = nBits
        self.nBytes = int( nBits / 8 )
        try:
            Eflag=dwf.FDwfDigitalInSampleFormatSet(self.hdwf[self.idx],c_int(self.nBits) )
            if (not Eflag):
                ErrMsg("\n faile to set the number of bits for sample \n")
        except ErrMsg as emsg:
            print emsg
            
    def DI_start_acquisition(self):
        try:
            # hdwf , bool Reconfigure=False, bool Start = True
            Eflag = dwf.FDwfDigitalInConfigure(self.hdwf[self.idx], c_bool(0), c_bool(1))
            if (not Eflag):
                raise ErrMsg("\ fail to start DI acquisition \n")
        except ErrMsg as emsg:
            print emsg
            
    def DI_read_buffer(self):
        sts = c_ubyte()
        finished = False
        while (not finished):
            try:
                Eflag = dwf.FDwfDigitalInStatus(self.hdwf[self.idx], c_int(1), byref(sts))
                if ( not Eflag):
                    raise ErrMsg("\n Fail to start acquisition  \n")
            except ErrMsg as emsg:
                print emsg
            if (sts.value == stsDone.value):
                finished = True
            time.sleep(1)
        try:
            #   buffer to copy the acquisition data / # of bytes to read ( each data has 2 bytes 
            Eflag=dwf.FDwfDigitalInStatusData(self.hdwf[self.idx], \
                self.rgwSamples, self.nBytes*self.cSamples*2 )
            if ( not Eflag ):
                raise ErrMsg("\n Fail to read out DI data buffer \n")
        except ErrMsg as emsg:
            print emsg
            
    def DI_read_record(self):
        sts = c_ubyte()
        cLost = c_int()
        cCorrupted=c_int()
        cAvailable = c_int()        
        fLost = 0
        fCorrupted = 0
        cSample = 0        
        while (cSample < self.cSamples):
            try:
                Eflag = dwf.FDwfDigitalInStatus(self.hdwf[self.idx], c_int(1), byref(sts))
                if ( not Eflag):
                    raise ErrMsg("\n Fail to start acquisition in read record  \n")
            except ErrMsg as emsg:
                print emsg
            if (cSample ==0 and (stsDwfStateConfig or sts==DwfStatePrefill or sts==DwfStateArmed)):
                continue  # not started
            try:
                Eflag=dwf.FDwfDigitalInStatusRecord(self.hdwf[self.idx], \
                    byref(cAvailable), byref(cLost), byref(cCorrupted) )
                if ( not Eflag ):
                    raise ErrMsg("\n Fail to read record DI data buffer \n")
            except ErrMsg as emsg:
                print emsg
            cSample += cLost.value
            
            if cLost.value:
                fLost = 1
            if cCorrupted.value:
                fCorrupted = 1
            if cAvailable.value ==0:
                continue
            if cSample + cAvailable.value > self.cSamples:
                cAvailable = c_int(self.cSamples - cSample)
            
            #now get samples
            try:
                Eflag = dwf.FDwfDigitalInStatusData(self.hdwf[self.idx], \
                byref(self.rgwSamples, self.nBytes*cSample), c_int(self.nBytes*cAvailable.value))
                if ( not Eflag ):
                    raise ErrMsg("\n fail to get record status data \n")
            except ErrMsg as emsg:
                print emsg
            cSample += cAvaible.value
            