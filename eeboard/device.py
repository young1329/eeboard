'''
EEBoard control based on Python
Coded by Youngsik Kim @Handong University
Updated to V0.7 @2020.11.17
	adding destruction
	The object should be del at the end to clear out the device handler
'''

from .dwfconstants import *
from ctypes import *
import time
import sys
if sys.platform.startswith("win"): # windows
    dwf=cdll.LoadLibrary('dwf.dll')
elif sys.platform.startswith('linux'): #linux
    dwf=cdll.LoadLibrary("libdwf.so")
else:   # max osx
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")

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
    def __init__(self,idx=0):
        if ( not(idx in Device.idDev) ):
            Device.idDev.append(idx)
            Device.hdwf.append(c_int(idx))
            Device.cDevice.append(c_int())
            Device.szDevName.append(create_string_buffer(64))
            Device.szSerialNum.append(create_string_buffer(16))
            Device.szName.append(create_string_buffer(32))
            Device.szLabel.append(create_string_buffer(16))
            Device.szUnits.append(create_string_buffer(16))

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

    def print_device_info(self,idx=0):
        for idx in Device.idDev:
            print('-------------------------------')
            print('Device %d'%(idx)+':'+Device.szDevName[idx].value.decode('utf-8')+'\t'+
                  Device.szSerialNum[idx].value.decode('utf-8'))


    def open_device(self,idx=0):
        szErr = create_string_buffer(512)
        try:
            if (idx in Device.idDev ):
                dwf.FDwfDeviceOpen(c_int(-1),byref(Device.hdwf[idx]))
                if (Device.hdwf[idx].value==0):
                    dwf.FDwfGetLastErrorMsg(szErr)
                    print(szErr.value)

                    raise ErrMsg("Device %d may not be connected properly"%(idx))
            else:
                raise ErrMsg('Device %d is not exist'%idx)

        except ErrMsg as emsg:
            print(emsg)

    def PCtrig(self):
        try:
            Eflag = dwf.FDwfDeviceTriggerPC(self.hdwf)
            if (not Eflag):
                raise ErrMsg("Failed to pc trigger in sceop\n")
        except ErrMsg as emsg:
            print(emsg)
        time.sleep(1)

    def CloseAll(self):
        dwf.FDwfDeviceCloseAll()


if __name__ == '__main__':

    import time

    dv=Device()
    dv.open_device()
    dv.get_device_info()
    dv.print_device_info()
    dv.CloseAll()
    del dv


