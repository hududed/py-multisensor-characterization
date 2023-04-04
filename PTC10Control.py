# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 10:38:37 2022

@author: Microprobe_Station
"""

import telnetlib

class PTC10Control:
    def __init__(self, host, port = 23, timeout=10):
        
        """Attempt to make connection with device, for the PTC the default
        port should be port 23"""
        self.host = host
        try:
            print(f"Connecting to PTC10 device at: {host}")
            self.tn = telnetlib.Telnet(host=host, port=port, timeout=timeout)
            print(f"Connected to PTC10 device at: {host}")
            self._variable_names = self.get_variable_names()
            self._power_variable_name = self._variable_names[0]
            self._temperature_variable_name = self._variable_names[2]
        except:
            print(f"Failed to connect to host at: {host}")
        
        
    def __del__(self):
        
        """Destructor -- Close the port in after the program has finished running
        
        Note that this is something that the telnetlib library will do on
        it's own, but for readibility this is included here."""
        print(f"Closing PTC10 at: {self.host}")
        self.tn.close()
        print(f"Successfully Closed PTC10 at: {self.host}")
        
        
        
    def _send_command(self, command:str):
        
        """Send a telnet command to the PTC10"""
        
        message = command + "\r\n"
        self.tn.write(message.encode())
        
    def _read_data(self):
        
        """Reads telnet response
        
        Note: this function should not be used for responseless commands as
        it will wait and read untill the device responds"""
        
        return self.tn.read_until(b'\r\n').decode('ascii')
    
    def get_variable_names(self)->list[str]:
        
        """Retrieve the defined variable names"""
        
        self._send_command('getOutput.names')
        names_as_string = self._read_data()
        names_as_list = names_as_string.split(',')
        return names_as_list
        
    def update_outputs(self)->list[float]:
        
        """Retrieve current output values"""
        
        self._send_command('getOutputs')
        outputs_as_string = self._read_data()
        self.outputs = [float(val) for val in outputs_as_string.split(',')]
        
        
        
    def enable_PID(self):
        
        """Turn on PID control loop"""
        
        command = self._power_variable_name + ".PID.mode = on"
        self._send_command(command)
        
    def disable_PID(self):
        
        """Turn of PID control loop"""
        
        command = self._power_variable_name + ".PID.mode = off"
        self._send_command(command)
        
    def temperature_setpoint(self, setpoint:float):
        
        """Set temperature setpoint"""
        
        command = self._power_variable_name + f".PID.setpoint = {setpoint}"
        self._send_command(command)
        
    def set_power(self, power:float):
        
        """Power value set by this function
        will be overwritten by PID if PID is still enabled"""
        
        command = self._power_variable_name + f".value = {power}"
        self._send_command(command)
        
        
    def enable_output(self):
        
        """Enables the output of device"""
        
        self._send_command('outputEnable on')
    
    def disable_output(self):
        
        """Disables the output of device"""
        
        self._send_command('outputEnable off')


#controller = PTC10('169.254.106.220')
#controller.temperature_setpoint(20)
#del controller
 

# def driver():
#     controller = PTC10Control('169.254.106.21')
#     time.sleep(1)
#     controller.temperature_setpoint(50)
#     time.sleep(1)
#     controller.enable_PID()
#     #controller.set_power(10)
    
# driver()
