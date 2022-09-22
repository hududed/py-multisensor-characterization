# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 18:19:00 2022

@author: Microprobe_Station
"""

from pyModbusTCP.client import ModbusClient
import time

def convert_word_to_binary(num:int)->str:
    
    """Convert modbus register to 16 bit word"""
    
    l = [int(b) for b in [*bin(num)[2:]]] #convert num to binary
    l.reverse()
    while len(l)<16:
        #fill in register to 16 bits
        l.append(0)
    l.reverse()
    l = [str(i) for i in l]
    l = "".join(l)
        
    return l

def set_bit(num:int,bit:int,bit_value:bool)->int:

    bit_value = str(int(bit_value))
    #l = [int(b) for b in [*bin(num)[2:]]]
    print(bin(num))
    l = list(convert_word_to_binary(num))
    l[len(l)-1-bit] = bit_value
    l = "".join(l)
    new_num = int(l,2)
    print(l)
    return new_num

def unsighned_transform(val):
    mask = (1 << 16) - 1
    if type(val) == int:  
        binary = bin(~(val ^ mask))
        return binary
    if type(val) == str:
        num = ~(int(val, 2) ^ mask)
        return num
    
def convert_from_unsigned(val):
    if val>32768:
        return val - 32768*2
    else:
        return val
    
def convert_to_unsigned(val):
    if val<0:
        return 32768*2+val
    else:
        return val
    
class EZTControl:
    def __init__(self, host):
        
        self.host = host
        try:
            print(f"Connecting to EZT device at: {host}")
            self.c = ModbusClient(host=host, port=502)
            print(f"Connected to EZT device at: {host}")
            self.update_modbus_registers()
        except ValueError:
            print("Error with host or port params")
            
    def __del__(self):
        print(f"Closing EZT at: {self.host}")
        self.c.close()
        print(f"Successfully Closed EZT at: {self.host}")
        
    def update_modbus_registers(self)->None:
        
        """Send and receive request for values from modbus registers 0 through
        73, register index values in this function are mapped in accordance 
        with mapping schema from EZT-430S Manual, pages 169-175
        
        When updated, values read from the device can be called as 
        class variables"""
        
        self.modbus_registers = self.c.read_holding_registers(0,73)
        
        #Byte Registers
        #B1
        self.system_status =                self.modbus_registers[0]
        #B2
        self.loop_communication_alarms =    self.modbus_registers[3]
        #B3
        self.loop_control_error_status =    self.modbus_registers[4]
        #B4
        self.process_alarm_status1 =        self.modbus_registers[5]
        self.process_alarm_status2 =        self.modbus_registers[6]
        #B5
        self.cntrl_loop_manual_ovride =     self.modbus_registers[9]
        #B6
        self.cntrl_loop_autotune_actvn =    self.modbus_registers[10]
        #B7
        self.system_events =                self.modbus_registers[12]
        #B10
        self.temp_op_status =               self.modbus_registers[38]
        self.hum_op_status =                self.modbus_registers[43]
        #B11
        self.temp_err_code =                self.modbus_registers[39]
        self.hum_err_code =                 self.modbus_registers[44]
        
        
        self.temp_PV =              convert_from_unsigned(self.modbus_registers[35])/10
        self.temp_SP =              convert_from_unsigned(self.modbus_registers[36])/10
        self.temp_output =          convert_from_unsigned(self.modbus_registers[37])/100
        self.hum_PV =               convert_from_unsigned(self.modbus_registers[40])/10
        self.hum_SP =               convert_from_unsigned(self.modbus_registers[41])/10
        self.hum_output =           convert_from_unsigned(self.modbus_registers[42])/100



    
    def enable_temperature_manual_mode(self)->None:
        self.update_modbus_registers()
        register_value = self.cntrl_loop_manual_ovride
        new_register_value = set_bit(register_value, bit = 0, bit_value=1)
        register = 9
        self.c.write_single_register(register, new_register_value)
    
    def disable_temperature_manual_mode(self)->None:
        self.update_modbus_registers()
        register_value = self.cntrl_loop_manual_ovride
        new_register_value = set_bit(register_value, bit = 0, bit_value=0)
        register = 9
        self.c.write_single_register(register, new_register_value)
        
    def enable_humidity_manual_mode(self)->None:
        self.update_modbus_registers()
        register_value = self.cntrl_loop_manual_ovride
        new_register_value = set_bit(register_value, bit = 1, bit_value=1)
        register = 9
        self.c.write_single_register(register, new_register_value)
    
    def disable_humidity_manual_mode(self)->None:
        self.update_modbus_registers()
        register_value = self.cntrl_loop_manual_ovride
        new_register_value = set_bit(register_value, bit = 1, bit_value=0)
        register = 9
        self.c.write_single_register(register, new_register_value)
        
        
        
    def set_temperature_SP(self, SP:float)->None:
        
        """Set the temperature setpoint
        
        SP: Setpoint value, round to 10th place"""
        
        SP = int(round(SP,1) * 10)
        SP = convert_to_unsigned(SP)
        register = 36
        self.c.write_single_register(register, SP)
        
    def set_humidity_SP(self, SP:float)->None:
        
        """Set the humidity setpoint
        
        SP: Setpoint value, rounded to 10th place"""
        
        SP = int(round(SP,1) * 10)
        SP = convert_to_unsigned(SP)
        register = 41
        self.c.write_single_register(register, SP)