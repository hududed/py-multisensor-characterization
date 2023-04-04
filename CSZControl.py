# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 18:19:00 2022

@author: Microprobe_Station
"""

from pyModbusTCP.client import ModbusClient
import time




try:
    c = ModbusClient(host='169.254.106.15', port=502)
except ValueError:
    print("Error with host or port params")
 
start_time = time.perf_counter()
if c.open():
    regs_list_1 = c.read_holding_registers(1,36)
    #regs_list_2 = c.read_holding_registers(40)
    #c.write_single_register(36, 100) 
    
    print(regs_list_1)
    #print(regs_list_2)
    
    c.close()


end_time = time.perf_counter()
print(end_time - start_time, "seconds")
    
class CSZControl:
    def __init__(self):
        try:
            self.c = ModbusClient(host='169.254.106.15', port=502)
        except ValueError:
            print("Error with host or port params")
            
    def __del__(self):
        
    def get_values(self)->list[float]:
        PV = c.read_holding_registers(0,50)
        PV = 
        
    def get_temperature_SP(self)->float:
        
    def set_temperature_SP(self, SP)->None:
        
    def get_humidity_PV(self)->float:
        
    def get_humidity_SP(self)->float:
        
    def set_humidity_SP(self, SP)->None: