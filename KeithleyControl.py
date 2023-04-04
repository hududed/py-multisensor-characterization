# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 08:43:42 2022

@author: Microprobe_Station
"""

import serial
import time
import pyperclip as pc
import numpy as np
import re
import pyperclip as pc


class Series2400SourceMeter:
    def __init__(self, com_port = 'COM6'):
        
        self.com_port = com_port
        print(f"Connecting to Keithley device at: {self.com_port}")
        
        self.ser = serial.Serial(self.com_port, 9600, timeout=1,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS,
                            )
        
        print(f"Connected to Keithley device at: {self.com_port}")
        
        # self.reset_errors()
        
    def __del__(self):
        print(f"Closing Keithley at: {self.com_port}")
        self.ser.close()
        print(f"Successfully Closed Keithley at: {self.com_port}")
        
    def resistance_mode(self):
        self.ser.write(b'*RST;')

        self.ser.write(b'FUNC "RES";')

        self.ser.write(b'RES:MODE AUTO;')
        
        self.ser.write(b':FORM:ELEM RES;')
        
    def point4_resistance(self):   
        self.ser.write(b':SYST:RSEN ON;')
        
    def read_value(self):
        self.ser.write(b':OUTP ON;')
        for i in range(10):   
            self.ser.write(b':READ?;')
        time.sleep(2)
        self.ser.write(b':OUTP OFF;')

        self.measurements = self.ser.read_all().decode("utf-8")[1::]
        parsed_measurements = [float(i) for i in self.measurements.split(';')]
        average_measurement = np.average(parsed_measurements)
        return average_measurement
    
    def disable_beep(self):
        self.ser.write(b':SYST:BEEP:STAT 0;')
        
    def reset_errors(self):
        self.ser.write(b'*CLS;')
        self.ser.write(b':STAT:PRES;')
        self.ser.write(b':STAT:QUE:CLE;')
        # self.ser.write(b':SYST:ERR:CLE;')
        
        

if __name__ == '__main__':
    srcm = Series2400SourceMeter()
    srcm.resistance_mode()
    srcm.point4_resistance()
    srcm.disable_beep()
    
    #%%
    
    M = []
    

    for i in range(5):
        v = srcm.read_value()
        count = 0
        print(v)
        M.append(v)
        
    print('Here is the mean, std:\n')
    print('_'*20)
    print('_'*20)
    print('')
    text = f'{np.average(M)}\t{np.std(M)}'
    print(text)
    pc.copy(text)
    print('')
    print('_'*20)
    print('_'*20)
    #%%
    # srcm.ser.write(b':SYST:CLE;')
    #%%
    time.sleep(1)
    srcm.__del__()


