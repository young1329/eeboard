Library for EEBoard

Digilentinc - Waveforms must be installed first

copy "eeboard" to any folder you like ex) /home/eeboard
and set PYTHONPATH environment variable
ex) export PYTHONPAHT=$PYTHONPAHT;/home/eeboard   on ubuntu

.
|-- Readme.txt   : this file
|-- eeboard
|   |-- __init__.py : package init file
|   |-- awg.py : AWG object
|   |-- device.py : Electronic Explorer board base class
|   |-- digitalio.py : digital static io object
|   |-- dwfconstants.py : constants provided from Digilentinc
|   |-- logic.py   : logic analyzer object
|   |-- pattern.py : digital pattern generation object
|   |-- power.py : Power supply and voltagemeter boject
|   `-- scope.py : analog scope object
`-- examples
    |-- 01_Device.py : check out the device connection.
    |-- 02_Power.py : Vref1, Vref2, VP+ and Voltage meters are tested
    |-- 03_AWG_Scope.py: AWG and Scope test
    |-- 04_DigitalIO.py : Static digital IO test
    |-- 05_Pattern_Logic03.py : 4bit counter and meausre with 8-bit 1000 samples with Single Acquisition Mode
    |-- 06_Pattern04.py D22 and D21 as output terminal, 1khz clock 50% duty output
    `-- 07_Pattern