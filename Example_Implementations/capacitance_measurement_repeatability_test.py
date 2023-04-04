# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 17:32:18 2022

@author: Microprobe_Station
"""




# c = []
# ct = []
# pt = []
# # def Driver():
# iet = IET7600Plus()

# iet.set_frequency(frequency=1000)

# iet.set_AC_test_type('V')
# iet.set_AC_signal_value(0.5)

from IET7600PlusControl import IET7600Plus
import numpy as np
import time
from PTC10Control import PTC10Control
from EZTControl import EZTControl
import csv
import re
import pandas as pd
#%%  
    
def SI_conversion_standard(unit:str):
    """Convert SI Prefix to SI no prefix"""
    
    if 'M' in unit:
        return 10**6
    elif 'k' in unit:
        return 10**3
    elif 'c' in unit:
        return 10**-2
    elif 'm' in unit:
        return 10**-3
    elif 'µ' in unit:
        return 10**-6
    elif 'n' in unit:
        return 10**-9
    elif 'p' in unit:
        return 10**-12
    elif 'f' in unit:
        return 10**-15

def SI_conversion_pF(unit:str):
    """Convert SI Prefix to SI no prefix"""
    
    if 'M' in unit:
        return 10**(6+12)
    elif 'k' in unit:
        return 10**(3+12)
    elif 'c' in unit:
        return 10**(-2+12)
    elif 'm' in unit:
        return 10**(-3+12)
    elif 'µ' in unit:
        return 10**(-6+12)
    elif 'n' in unit:
        return 10**(-9+12)
    elif 'p' in unit:
        return 10**(-12+12)
    elif 'f' in unit:
        return 10**(-15+12)
    
wait_time = 20*60
platform_temp_record = []
chamber_temp_record = []

#def driver():
    
ptc10 = PTC10Control('169.254.106.13')
ezt = EZTControl('169.254.106.15')
iet = IET7600Plus()
start_time = time.time()

iet.set_frequency(frequency=1000)
iet.set_num_avg(5)
iet.measure_data() 

time.sleep(5)

def set_temperature(temp):
    ezt.set_temperature_SP(temp)
    ptc10.temperature_setpoint(temp)
    
def get_iet_data(SI_conversion:object):    
    unfiltered_data = iet.measure_data()
    number = re.search('(\d*\.?\d+)',unfiltered_data).group(1)
    Farad_SI_unit = re.search('(\wF)',unfiltered_data).group(1)
    return float(number) * SI_conversion(Farad_SI_unit)
 

ptc10.enable_PID()
ptc10.enable_output()

#Make file -------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
date = time.asctime().replace(':','_')
file_name = f'Temperature Capacitance Profile _{date}.csv'

fields_names=['Time (s)',
              'Time (min)',
              'Time (hr)',
            'Chamber Temperature SP (°C)', 
            'Chamber Temperature (°C)', 
            'Platform Temperature SP',
            'Platform Temperature (°C)',
            'Chamber Relative Humidity SP (% RH)',
            'Chamber Relative Humidity (% RH)',
            'Chamber Temperature Output (%)',
            'Platform Output (%)',
            'Chamber Humidity Output (%)',
            'Capacitance (F)',
            'Capacitance (pF)']

# with open(file_name, 'a', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(fields_names)
print(fields_names)
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

# set_temperature(60)
# time.sleep(60*20)

# set_temperature(-20)
# time.sleep(60*40)

fields_list = []

def temperature_setpoint_time(temperature, delay_time):
    
    set_temperature(temperature)
    
    for i in range(delay_time):
        
        
        ptc10.update_outputs()
        ezt.update_modbus_registers()
        
        chamber_temperature = ezt.temp_PV
        chamber_humidity = ezt.hum_PV
        chamber_t_output = ezt.temp_output
        chamber_h_output = ezt.hum_output
        platform_temperature_SP = ptc10.temperature_setpoint
        platform_temperature = ptc10.outputs[1]
        platform_output = ptc10.outputs[0]/50*100
        platform_temp_record.append(platform_temperature)
        
        
            
        # capacitance_F = get_iet_data(SI_conversion_standard)
        capacitance_pF = get_iet_data(SI_conversion_pF)
        capacitance_F = capacitance_pF/10**12
        
        measure_time = time.time() - start_time
        fields = [measure_time,
                  measure_time/60,
                  measure_time/60,
                  ezt.temp_SP, 
                  chamber_temperature,
                  platform_temperature_SP,
                  platform_temperature,
                  ezt.hum_SP,
                  chamber_humidity, 
                  chamber_t_output,
                  platform_output,
                  chamber_h_output, 
                  capacitance_F,
                  capacitance_pF]
        
        fields_list.append(fields)
        print(fields)
        # with open(file_name, 'a',newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(fields)
            
        time.sleep(5)
#SP at given temperature for 20 minutes each time (10*20*6 seconds sleep time == 1200==20 minutes)
#average processing time is 0.121758557

magnitude = 30

#one state per 3 hours
###########################THIS SHOULD FINISH MONDAY EVENING 9/5/2022
temperature_setpoint_time(50,1243)
temperature_setpoint_time(0,1243)
temperature_setpoint_time(50,1243)
temperature_setpoint_time(0,1243)
temperature_setpoint_time(50,1243)
temperature_setpoint_time(0,1243)

temperature_setpoint_time(50,1243)
temperature_setpoint_time(40,1243)
temperature_setpoint_time(50,1243)
temperature_setpoint_time(40,1243)
temperature_setpoint_time(50,1243)
temperature_setpoint_time(40,1243)

temperature_setpoint_time(10,1243)
temperature_setpoint_time(0,1243)
temperature_setpoint_time(10,1243)
temperature_setpoint_time(0,1243)
temperature_setpoint_time(10,1243)
temperature_setpoint_time(0,1243)

temperature_setpoint_time(20,1243)
temperature_setpoint_time(30,1243)
temperature_setpoint_time(20,1243)
temperature_setpoint_time(30,1243)
temperature_setpoint_time(20,1243)
temperature_setpoint_time(30,1243)

temperature_setpoint_time(20,1243)
temperature_setpoint_time(40,1243)
temperature_setpoint_time(20,1243)
temperature_setpoint_time(40,1243)
temperature_setpoint_time(20,1243)
temperature_setpoint_time(40,1243)
        
ptc10.__del__()
ezt.__del__()
iet.__del__()

data = pd.DataFrame(fields_list)
data.columns = fields_names
data.to_csv(file_name)
#driver()
