##Multisensor Characterization System
The Multisensor Characterization System is a control system for electrical characterizations. It is designed to acquire data from four different hardware devices:

LCR meter (IET 7600 Plus)
CSZ humidity chamber (MCBH 1.2-.33-H/AC)
Stanford Research temperature controller (PTC10)
Keithley 2400 MultiMeter
This repository provides example implementations for controlling all four devices.

#Table of Contents
Installation
Usage
Dependencies
Examples
Contributing
#License
#Installation
To install the Multisensor Characterization System, clone this repository to your local machine using the following command:

bash
Copy code
git clone https://github.com/MattTMuller/py-multisensor-characterization.git
Usage
To use the Multisensor Characterization System, follow these steps:

Connect the hardware devices to your computer as specified in the documentation for each device.
Install the dependencies for the system (see Dependencies below).
Open the example implementation for the device you want to use (in the Example_Implementations folder) and run the code.
Follow the instructions in the code to perform the desired sensor characterization.
Dependencies
The Multisensor Characterization System requires the following dependencies:

Python 3.6 or higher
PyVISA library
NumPy library
pyserial
pymodbus
To install the dependencies, run the following command:

bash
Copy code
pip install pyvisa numpy pyserial pymodbus
Examples
The Example_Implementations folder contains working files to build off of to control all four devices. These files can be used as a starting point for building your own implementations for the Multisensor Characterization System.

Contributing
If you would like to contribute to the Multisensor Characterization System, please follow these guidelines:

Fork the repository.
Create a new branch for your feature or bug fix.
Write tests for your changes.
Make your changes and ensure all tests pass.
Submit a pull request.
License
The Multisensor Characterization System is released under the Apache License.