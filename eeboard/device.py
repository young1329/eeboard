''' 
EEBoard control based on Python
Coded by Youngsik Kim @Handong University
Updated to V06 @2018.09.12
	adding destruction
	The object should be del at the end to clear out the device handler
'''

from dwfconstants import *
from ctypes import *
import time
import sys
if sys.platform.startswith("win"):
    dwf=cdll.dwf
else:
    dwf=cdll.LoadLibrary("libdwf.so")

class ErrMsg(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.msg
        
# Device class : System, Device group : detection, get info open / close
class Device():    
    idDev=[];
    hdwf=[]; cDevice=[];szDevName=[];szSerialNum=[];szLabel=[];szName=[];szUnits=[];
    szVersion = create_string_buffer(16)
    def __init__(self,idx=-1):
        if ( not(idx in Device.idDev) ):
            Device.idDev.append(idx)
            Device.hdwf.append(c_int(idx))
            Device.cDevice.append(c_int())
            Device.szDevName.append(create_string_buffer(64))
            Device.szSerialNum.append(create_string_buffer(16))
            Device.szName.append(create_string_buffer(32))
            Device.szLabel.append(create_string_buffer(16))
            Device.szUnits.append(create_string_buffer(16))
        else :
            print('passed in device')
            pass
        
    def __del__(self):
        for idx in Device.idDev:
            dwf.FDwfDeviceClose(Device.hdwf[idx])
            print("Device %d is closed\n"%(idx))

    def get_device_info(self,idx=0):
        if ( idx in Device.idDev ):
            dwf.FDwfEnum(c_int(idx),byref(Device.cDevice[idx]))       # Get the first(0) EEboard handler
            dwf.FDwfEnumDeviceName(c_int(idx),Device.szDevName[idx])  # Get the EEboard Name
            dwf.FDwfEnumSN(c_int(idx),Device.szSerialNum[idx])           #Get the seiral number
            dwf.FDwfGetVersion(Device.szVersion)                  # Get the version info

    def print_device_info(self):
        for idx in Device.idDev:
            print('-------------------------------')
            print('Device %d'%(idx)+':'+Device.szDevName[idx].value+'\t'+
                  Device.szSerialNum[idx].value)
            
        
    def open_device(self,idx=-1):
        szErr = create_string_buffer(512)
        try:
            hdwf=c_int()
            if (idx in Device.idDev ):
                dwf.FDwfDeviceOpen(c_int(idx),byref(hdwf))
                print(Device.hdwf[idx].value)
                if (Device.hdwf[idx].value==0):
                    dwf.FDwfGetLastErrorMsg(szErr)
                    print szErr.value
                    raise ErrMsg("Device %d may not be connected properly"%(idx))
                else:
                    Device.hdwf[idx]=hdwf
            else:
                raise ErrMsg('Device %d is not exist'%idx)
            
        except ErrMsg as emsg:
            print emsg

    def PCtrig(self):
        try:
            Eflag = dwf.FDwfDeviceTriggerPC(self.hdwf)
            if (not Eflag):
                raise ErrMsg("Failed to pc trigger in sceop\n")
        except ErrMsg as emsg:
            print emsg
        time.sleep(1)

    def CloseAll(self):
        dwf.FDwfDeviceCloseAll()

    # Desctructor
    def __del__(self):
        dwf.FDwfDeviceCloseAll()        #close out eeboard
