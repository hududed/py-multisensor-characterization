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
# delimiters = "a", ",", "(c)"
# example = "stackoverflow (c) is awesome... isn't it?"
# regex_pattern = '|'.join(map(re.escape, delimiters))



# column_number = 0#input('Column Number:')
# line_number = 0#input('Line Number:') #lines start at zero

# file_name = 'column{} line {} resistance_measurements.csv'.format(column_number, line_number)


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
        #set device to measure resistance
        self.ser.write(b'FUNC "RES";')
        #set scaling mode to auto
        self.ser.write(b'RES:MODE AUTO;')
        
        self.ser.write(b':FORM:ELEM RES;')
        
    def read_value(self):
        self.ser.write(b':OUTP ON;')
        for i in range(10):   
            self.ser.write(b':READ?;')
        time.sleep(3)
        self.ser.write(b':OUTP OFF;')
        #self.ser.read_until()
        #time.sleep(2)
        self.measurements = self.ser.read_all().decode("utf-8")[1:-1]
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
        
# srcm = Series2400SourceMeter()

# #%%
# srcm.resistance_mode()
# srcm.disable_beep()
# #%%
# for i in range(15):
#     v = srcm.read_value()
#     x = srcm.measurements
#     #time.sleep(2)
#     y = srcm.ser.read_all().decode("utf-8")[1:-1]
#     #time.sleep(7)
# #%%
# srcm.ser.write(b':SYST:CLE;')
# #%%

# del srcm

