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
#%%
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
            'Chamber Humidity Output (%)',
            'Capacitance (F)',
            'Capacitance (pF)']

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
        capacitance_pF = get_iet_data(SI_conversion_pF)
        capacitance_F = capacitance_pF/10**12
        
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
                  chamber_h_output, 
                  capacitance_F,
                  capacitance_pF]
        
        fields_list.append(fields)
        print(fields)

            
        time.sleep(5)


# # time.sleep(60*30)
# for humidity in np.linspace(0,90,200):
#     enviornment_setpoint_time(22, humidity, 10)
set_temperature(30)
ezt.set_humidity_SP(1)
time.sleep(60*30)
set_temperature(0)
time.sleep(60*20)

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
set_temperature(5)
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





if max(data['Time (hr)'])>2:
    t_axis = 'Time (hr)'
elif max(data['Time (min)']>2):
    t_axis = 'Time (hr)'
else:
    t_axis = 'Time (s)'

#%%
# create figure and axis objects with subplots()
fig,ax = plt.subplots()
# make a plot
# ax.plot(data[t_axis],
#         data['Chamber Temperature SP (°C)'],
#         color="green", 
#         )
ax.plot(data[t_axis],
        data['Platform Temperature (°C)'],
        color="red", 
        )
# ax.plot(data[t_axis],
#         data['Chamber Temperature (°C)'],
#         color="green", 
#         )

# set x-axis label
ax.set_xlabel(t_axis, fontsize = 14)
# set y-axis label
ax.set_ylabel("Temperature (°C)",
              color="red",
              fontsize=14)

plt.legend(['SP', 'Platform'], loc='upper left')

# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(data[t_axis], data['Capacitance (pF)'],color="blue")
ax2.set_ylabel("Capacitance (pF)",color="blue",fontsize=14)
plt.title('Temperature and Capacitance vs. Time')
plt.show()
# save the plot as a file
fig.savefig(f'{file_directory}\\Humidity and Capacitance vs. Time - {file_name}.jpg',
            format='jpeg',
            dpi= 1200,
            bbox_inches='tight')

# create figure and axis objects with subplots()
fig,ax = plt.subplots()
# make a plot
# ax.plot(data[t_axis],
#         data['Chamber RH SP (% RH)'],
#         color="yellow", 
#         )
ax.plot(data[t_axis],
        data['Chamber RH (% RH)'],
        color="red", 
        )


# set x-axis label
ax.set_xlabel(t_axis, fontsize = 14)
# set y-axis label
ax.set_ylabel("Chamber Relative Humidity (% RH)",
              color="red",
              fontsize=14)

# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(data[t_axis], data['Capacitance (pF)'],color="blue")
ax2.set_ylabel("Capacitance (pF)",color="blue",fontsize=14)
plt.title('Humidity and Capacitance vs. Time')
plt.show()
# save the plot as a file
fig.savefig(f'{file_directory}\\Temperature and Capacitance vs. Time - {file_name}.jpg',
            format='jpeg',
            dpi= 1200,
            bbox_inches='tight')

#%%
plt.figure(dpi=1200)

plt.hist2d(y = data['Capacitance (pF)'], x=data['Chamber RH (% RH)'], bins=100)
plt.colorbar()
plt.title('Capacitance vs. RH Histogram')
plt.ylabel('Capacitance (pF)')
plt.xlabel('Relative Humidity (%)')
plt.savefig(f'{file_directory}\\2D Histogram CvH - {file_name}.jpeg',format='jpeg',
            dpi= 1200,
            bbox_inches='tight')

plt.figure(dpi=1200)
plt.scatter(y = data['Capacitance (pF)'], x=data['Chamber RH (% RH)'])
plt.title('Capacitance vs. Humidity')
plt.ylabel('Capacitance (pF)')
plt.xlabel('Relative Humidity (%)')
plt.savefig(f'{file_directory}\\Scatter Plot CvH- {file_name}.jpeg',format='jpeg',
            dpi= 1200,
            bbox_inches='tight')


#%%
plt.figure(dpi=1200)
plt.hist2d(y = data['Capacitance (pF)'], x=data['Platform Temperature (°C)'], bins=100)
plt.colorbar()
plt.title('Capacitance vs. Temperature')
plt.ylabel('Capacitance (pF)')
plt.xlabel('Platform Temperature (°C)')
plt.savefig(f'{file_directory}\\2D Histogram CvT- {file_name}.jpeg',format='jpeg',
            dpi= 1200,
            bbox_inches='tight')



plt.figure(dpi=1200)
plt.scatter(y = data['Capacitance (pF)'], x=data['Platform Temperature (°C)'])
plt.title('Capacitance vs. Temperature')
plt.ylabel('Capacitance (pF)')
plt.xlabel('Platform Temperature (°C)')
plt.savefig(f'{file_directory}\\Scatter Plot CvT- {file_name}.jpeg',format='jpeg',
            dpi= 1200,
            bbox_inches='tight')

#%%

def wind_down():    
    print('Winding Down')
    ezt.set_humidity_SP(20)
    ezt.set_temperature_SP(40)
    time.sleep(60*30)
    set_temperature(10)
#%%

ezt.set_humidity_SP(1)
time.sleep(60*20)
set_temperature(0)
time.sleep(60*20)

#%%   
ptc10.__del__()
ezt.__del__()
iet.__del__()
#driver()


















