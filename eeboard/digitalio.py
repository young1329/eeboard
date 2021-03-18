'''
EEBoard control based on Python
Coded by Youngsik Kim @Handong University
Updated to V0.7 @2020.11.17
	adding destruction
	The object should be del at the end to clear out the device handler
'''

from .device import *


class DigitalIO(Device):

    def __init__(self,idx=0):
        self.idx = idx;
        Device.__init__(self,idx)
        self.pfsOutput =c_uint32()
        self.OutputPins = c_uint32()
        self.OutputValues = c_uint32()
        self.InputValues = c_uint32()

    def Reset_DIO(self):
        # reset and configure by default(all digital Tri-state)
        try:
            Eflag = dwf.FDwfDigitalIOReset(self.hdwf[self.idx])
            if (not Eflag):
                raise ErrMsg("\n Digital IO Reset Error\n")
        except ErrMsg as emsg:
            print(emsg)

    def SetOutputPins(self,out_pins):
        try:
            Eflag = dwf.FDwfDigitalIOOutputEnableSet(self.hdwf[self.idx],c_int(out_pins))
            self.OutputPins = out_pins
            if (not Eflag):
                raise ErrMsg("\n Set Output Pin Setup\n")
        except ErrMsg as emsg:
            print(emsg)

    def SetOutputValues(self,output_values):
        try:
            self.OutputValues = output_values
            Eflag = dwf.FDwfDigitalIOOutputSet(self.hdwf[self.idx],self.OutputValues)
            if (not Eflag):
                raise ErrMsg("\n Set Output values failed \n")
        except ErrMsg as emsg:
            print(emsg)

    def GetDigitalIOInputs(self):
        try:
            Eflag = dwf.FDwfDigitalIOStatus(self.hdwf[self.idx])
            Eflag = Eflag & dwf.FDwfDigitalIOInputStatus(self.hdwf[self.idx],byref(self.InputValues))
            if (not Eflag):
                raise ErrMsg("\n Digital IO Inputs reading error\n")
        except ErrMsg as emsg:
            print(emsg)