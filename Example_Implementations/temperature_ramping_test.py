# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 16:15:45 2022

@author: toddm
"""

from PTC10Control import PTC10Control
from EZTControl import EZTControl
import numpy as np
import pandas as pd
import time
import csv
#%%



def driver():
    ptc10 = PTC10Control('169.254.106.13')
    ezt = EZTControl('169.254.106.15')
    start_time = time.time()
    
    def set_temperature(temp):
        ezt.set_temperature_SP(temp)
        ptc10.temperature_setpoint(temp)
 
    set_temperature(50)
    ptc10.enable_PID()
    ptc10.enable_output()
    
    
    date = time.asctime().replace(':','_')
    file_name = f'Temperature Profiles_{date}.csv'
    
    fields=['Time (s)','Chamber Temperature SP (°C)', 
            'Chamber Temperature (°C)', 
            'Platform Temperature (°C)',
            'Chamber Output (%)',
            'Platform Output (%)']
    
    with open(file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        
    platform_temp_record = []
    

    
    for i in range(10):
         
        ptc10.update_outputs()
        ezt.update_modbus_registers()
        ambient_temperature = ezt.temp_PV
        ambient_output = ezt.temp_output
        platform_temperature = ptc10.outputs[1]
        platform_output = ptc10.outputs[0]/50*100
        platform_temp_record.append(platform_temperature)
        
        
        if len(platform_temp_record)>100:
            platform_std = np.std(platform_temp_record[-100:])
            platform_avg = np.mean(platform_temp_record[-100:])
            percent_deviation = platform_std/platform_avg
            print(percent_deviation)
            if percent_deviation<0.01:
                set_temperature(0)
                
                
        print(ambient_temperature)
        print(platform_temperature)
        print(ezt.temp_SP)
        
        measure_time = time.time() - start_time
        fields = [measure_time, ezt.temp_SP, ambient_temperature, platform_temperature, ambient_output, platform_output]
        fields
        with open(file_name, 'a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            
        time.sleep(5)

driver()


    