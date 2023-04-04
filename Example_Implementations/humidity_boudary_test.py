# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 17:27:15 2022

@author: Microprobe_Station
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:13:43 2022

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
import re


#%%  
    

    
wait_time = 20*60
platform_temp_record = []
chamber_temp_record = []

#def driver():
    
ptc10 = PTC10Control('169.254.106.13')
ezt = EZTControl('169.254.106.15')
start_time = time.time()
#%%


time.sleep(5)

def set_temperature(temp):
    ezt.set_temperature_SP(temp)
    ptc10.temperature_setpoint(temp)
    
 

ptc10.enable_PID()
ptc10.enable_output()

#Make file -------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
date = time.asctime().replace(':','_')


fields_names=['Time (s)',
              'Time (min)',
              'Time (hr)',
            'Chamber Temperature SP (°C)', 
            'Chamber Temperature (°C)', 
            'Platform Temperature (°C)',
            'Chamber RH SP (% RH)',
            'Chamber RH (% RH)',
            'Chamber Temperature Output (%)',
            'Platform Output (%)',
            'Chamber Humidity Output (%)']

print(fields_names)

fields_list = []

def enviornment_setpoint_time(temperature, humidity, delay_time):
    

    set_temperature(temperature)
    ezt.set_humidity_SP(humidity)
    
    for i in range(delay_time):
        
        print(f'Loop Number: {i}')
        
        ptc10.update_outputs()
        ezt.update_modbus_registers()
        
        chamber_temperature = ezt.temp_PV
        chamber_humidity = ezt.hum_PV
        chamber_t_output = ezt.temp_output
        chamber_h_output = ezt.hum_output
        platform_temperature = ptc10.outputs[1]
        platform_output = ptc10.outputs[0]/50*100
        platform_temp_record.append(platform_temperature)
        
        
            
        # capacitance_F = get_iet_data(SI_conversion_standard)
        
        measure_time = time.time() - start_time

        fields = [measure_time,
                  measure_time/60,
                  measure_time/60/60,
                  ezt.temp_SP, 
                  chamber_temperature,
                  platform_temperature,
                  ezt.hum_SP,
                  chamber_humidity, 
                  chamber_t_output,
                  platform_output,
                  chamber_h_output]
        
        fields_list.append(fields)
        print(fields)

            
        time.sleep(5)


# # time.sleep(60*30)
# for humidity in np.linspace(0,90,200):
#     enviornment_setpoint_time(22, humidity, 10)
# set_temperature(30)
# ezt.set_humidity_SP(1)
# time.sleep(60*30)
# set_temperature(0)
# time.sleep(60*5)

for temp in np.linspace(0,50,10):
    enviornment_setpoint_time(temp, 1, 100)

set_temperature(0)
time.sleep(60*20)
ezt.set_humidity_SP(99)
time.sleep(60*20)

for temp in np.linspace(0,50,10):
    enviornment_setpoint_time(temp, 99, 100)
    
ezt.set_humidity_SP(1)
time.sleep(60*40)
set_temperature(0)
time.sleep(60*20)



#%%

from pathlib import Path
import os
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import pandas as pd

file_name = f'Humidity Boundary_{date}'

read_me = """The purpose of this test is to identify the maximum and minimum 
humidity values that can be acheived at temperatures in the range of 0 to 50C,
Here is the code used to perform the operations:
for temp in np.linspace(0,50,100):
    enviornment_setpoint_time(temp, 1, 10)

set_temperature(0)
time.sleep(60*20)
ezt.set_humidity_SP(99)
time.sleep(60*20)

for temp in np.linspace(0,50,100):
    enviornment_setpoint_time(temp, 99, 10)
    
ezt.set_humidity_SP(1)
time.sleep(60*20)
set_temperature(0)
time.sleep(60*20)"""

 

 
path = Path(os.getcwd())
parent_directory = path.parent.absolute()
file_directory = os.path.join(parent_directory, file_name)

if not os.path.exists(file_directory):
    os.mkdir(file_directory)
    print("Directory '% s' created" % file_directory)

#%%
data = pd.DataFrame(fields_list)
data.columns = fields_names
data.to_csv(f'{file_directory}\\Table - {file_name}.csv')
#%%

f = open(f'{file_directory}\\Experiment Notes.txt', "w")
f.write(read_me)
f.close()

#%%
with pd.ExcelWriter(f'{file_directory}\\Correlation Table - {file_name}.xlsx') as writer:
    data.corr().to_excel(writer, sheet_name='Correlation Table')
    for column in data.columns:
        df = data.corr()[column].sort_values(ascending=False)
        df.to_excel(writer, sheet_name=column)
#%% 



#%%





#%%


temp_sets = list(data.groupby('Chamber Temperature SP (°C)'))
temp = []
rh_low = []
rh_high = []

for tup in temp_sets:
    
    temperature, df = tup
    temp.append(temperature)
    rh_low.append(min(df['Chamber RH (% RH)']))
    rh_high.append(max(df['Chamber RH (% RH)']))


import pandas as pd
boundaries = pd.DataFrame(dict({'Temperature':temp, 'RH Low': rh_low, 'RH High':rh_high}))
boundaries.to_csv(f'{file_directory}\\Boundary Table- {file_name}.csv')
#%%
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

plt.figure(dpi=1200)

plt.plot(boundaries['Temperature'], boundaries['RH High'])
plt.plot(boundaries['Temperature'], boundaries['RH Low'])



plt.title('Humidity Boundary Plot')
plt.ylabel('Relative Humidity (%)')
plt.xlabel('Chamber Temperature (°C)')
plt.legend(['RH High', 'RH Low'])

plt.savefig(f'{file_directory}\\Boundary Plot- {file_name}.jpeg',format='jpeg',
            dpi= 1200,
            bbox_inches='tight')


#%%


#Wind down
ezt.set_humidity_SP(1)
time.sleep(60*20)
set_temperature(0)
time.sleep(60*20)



#%%   
ptc10.__del__()
ezt.__del__()
#driver()


















