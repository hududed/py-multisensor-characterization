# Multisensor Characterization System
The Multisensor Characterization System is a control system for electrical characterizations. It is designed to acquire data from four different hardware devices:

- LCR meter (IET 7600 Plus)
- CSZ humidity chamber (MCBH 1.2-.33-H/AC)
- Stanford Research temperature controller (PTC10)
- Keithley 2400 MultiMeter
This repository provides example implementations for controlling all four devices.

## Table of Contents
1. Installation
2. Usage
3. Dependencies
4. Examples
5. Contributing
6.  License
## Installation
To install the Multisensor Characterization System, clone this repository to your local machine using the following command:

In the terminal:  

`git clone https://github.com/MattTMuller/py-multisensor-characterization.git`

## Usage
To use the Multisensor Characterization System, follow these steps:

1. Connect the hardware devices to your computer as specified in the documentation for each device.
2. Install the dependencies for the system (see Dependencies below).
3. Open the example implementation for the device you want to use (in the Example_Implementations folder) and run the code.
4. Follow the instructions in the code to perform the desired sensor characterization.

## Dependencies
The Multisensor Characterization System requires the following dependencies:

Python 3.6 or higher
PyVISA library
NumPy library
pyserial
pymodbus
To install the dependencies, run the following command:

In the terminal:

`pip install pyvisa numpy pyserial pymodbus`

## Examples
The `Example_Implementations` folder contains working files to build off of to control all four devices. These files can be used as a starting point for building your own implementations for the Multisensor Characterization System.

## Contributing
If you would like to contribute to the Multisensor Characterization System, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write tests for your changes.
4. Make your changes and ensure all tests pass.
5. Submit a pull request.

## License
The Multisensor Characterization System is released under the Apache License.
