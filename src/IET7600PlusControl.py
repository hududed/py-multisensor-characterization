# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 09:23:46 2022

@author: Microprobe_Station
"""

import serial
import time

#frequency is units of Hz and has range of 10 to 2000000 (2MHz)
#voltage is units of V and has range of 0.02V to 5V
#current is units of A and has a range of 0.000250 microamps to 0.1 A

# #%%
# ser = serial.Serial('COM1', 9600, timeout=1,
#                     parity=serial.PARITY_NONE,
#                     stopbits=serial.STOPBITS_ONE,
#                     bytesize=serial.EIGHTBITS,
#                     )
# # ser.write(b'conf:freq 2000\n')

# ser.write(b'conf:ppar cs\n')
# #%%
# ser.write(b'conf:spar n\n')
# #%%
# ser.write(b'conf:swe:swe on\n')
# ser.write(b'conf:swe:par i\n')
# ser.write(b'conf:swe:step 25\n')
# ser.write(b'conf:swe:beg 0.000250\n')
# ser.write(b'conf:swe:end 0.1\n')
# ser.write(b'MEAS\n')
# #%%
# ser.write(b'FETC?\n')
# #%%
# text = ser.read_until('\n').decode("utf-8")
# print(text)
# #%%
# ser.write(b'conf:swe:beg 100.0\n')
# ser.write(b'conf:swe:end 1000\n')


# ser.write(b'MEAS:\n')
# #%%
# ser.close()
#%%
class IET7600Plus:
    def __init__(self, com_port='COM1'):
        
        """Attempt to make connection with device"""
        
        self.com_port = com_port
        
        print(f"Connecting to IET device at: {self.com_port}")
        self.ser = serial.Serial(com_port, 9600, timeout=1,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                )
        print(f"Connected to IET device at: {self.com_port}")
            
        #self.measure_data() #prime the IET register with data
        # except:
        #     print(f"Failed to connect to host at: {self.com_port}")
        
        
    def __del__(self):
        
        """Destructor -- Close the port in after the program has finished running
        
        Note that this is something that the telnetlib library will do on
        it's own, but for readibility this is included here."""
        print(f"Closing IET7600 at: {self.com_port}")
        self.ser.close()
        print(f"Successfully Closed IET7600 at: {self.com_port}")
        
        
        
    def _send_command(self, command:str):
        
        """Send a telnet command to the IET"""
        
        message = command + "\n"
        self.ser.write(message.encode())
        
    def _read_data(self):
        
        """Reads serial response
        
        Note: this function should not be used for responseless commands as
        it will wait and read untill the device responds"""
        
        data = self.ser.read_until(b'\n').decode("utf-8")
        return data
    
    def measure_data(self, measurement_dalay:float = 1) -> str:
        
        """""Function:
            
            Send request for device to measure a value, send the value over
            the serial connection. Function will return 
            
            Parameters:
                measurement_delay: delay between read time, minimum of 0.5
                seconds is required."""
            
        time.sleep(measurement_dalay)
        self._send_command('MEAS')
        self._send_command('FETC?\n')
        return self._read_data()

    
    #configure
    def set_frequency(self, frequency:int):
        """Function:
            Set the frequency from 10 to 2000000 Hz
            
        Parameters:
            0000000.00 
                """
                
        self._send_command(f'conf:freq {frequency}')
        
    def set_primary_param(self,parameter:str):
        """Function:
            Set the primary parameter
            
        Parameters:
            A(auto) CS CP LS 
            LP RP RS DF Q Z Y 
            P(phase angle) ESR 
            GP XS BP
        """
        
        self._send_command(f'conf:ppar {parameter}')
            
    def set_secondary_param(self, parameter):
        
        """Function:
            Set the secondary parameter
            
        Parameters:
            N(none) CS CP LS 
            LP RP RS DF Q Z Y 
            P(phase angle) ESR 
            GP XS BP    
        """
        
        self._send_command(f'conf:spar {parameter}')
        
    def set_AC_test_type(self, test:str):
        
        """Function:
            Set the AC test signal type.
            
        Note: This should be set prior to setting the AC Value
        
        Parameters:
            
            test: Voltage (V) or Current (I)"""
            
        self._send_command(f'conf:acty {test}')
        
    def set_AC_signal_value(self, value:float):
        
        """Function:
            Set the AC signal toa specified value
            
        Parameters:
            floating point value, if AC test signal is set to 
            voltage then AC signal is between 0.02 and 5
            if AC signal is set to current then AC signal is between 
            0.000250 and 0.1"""

        self._send_command(f'conf:acv {value}')
            
    def set_bias(self, bias:str):
        """Function:
            Set the bias
            
        Parameters:
            INT EXT or OFF
            """
        
        self._send_command(f'conf:bias {bias}')
            
    def set_range(self, ran:str):
        """Function:
            Set the range
            
        Parameters:
            ATUTO HOLD or #(1-59)"""
        
        self._send_command(f'rang:conf {ran}')
        
    def set_meas_accuracy(self, accuracy:str):
        """Function:
            Set the measurement accuracy
        Parameters:
            SLO MED FAS
            """
            
        self._send_command(f'conf:mac {accuracy}')
        
    def set_meas_delay(self, delay:int):
        
        """Function:
            
        Parameters:
            
            """
        self._send_command(f'conf:tdel {delay}')
        
    def set_num_avg(self, average:int) -> None:
        
        """Function:
            
        Parameters:
            
            """
        self._send_command(f'conf:aver {average}')
        #self.measure_data()
        
    # def set_med_fncn(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def set_distortion(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def set_contact_check(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def set_disp_type(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def set_trigger(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def set_nominal(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # #Binning
    
    # def set_bin_limit(self, bin_number, ):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def set_bin_tolerance(self, bin_number,):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def set_secondary_bin_limit(self, bin_number,):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def reset_bin(self, bin_number,):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def summary(self, bin_number,):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def set_bin_result_format(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def set_bin_handler_port(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def bin_print_result(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def bin_file_to_usb(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def bin_file_duplicate(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def bin_file_new(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def bin_file_append(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def bin_close(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    def sweep_parameter(self, param: str) -> None:
        """Function: Define parameter to sweep
            
        Parameters:
        F: frequency
        V: voltage
        I: current
        """
        self._send_command(f'conf:swe:par {param}')

    def sweep_begin(self, param_value: float) -> None:
                
        """Function: Define begin value for sweep
        """
        self._send_command(f'conf:swe:beg {param_value}')
    # def sweep_end(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def sweep_step(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def sweep_display(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    def sweep_enable(self, toggle_param: str='ON') -> None:
        """Function:
            Set the sweep function ON or OFF
            
        Parameters:
        """
        self._send_command(f'conf:swe:swe {toggle_param}')
    # def sweep_valid(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    
    # def file_save(self, method):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def file_recall(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def file_valid(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def sequence_ebable(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def sequence_test(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def sequence_frequency(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def sequence_primary_parameter(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
    # def sequence_second_parameter(self):
                
    #     """Function:
            
    #     Parameters:
            
    #         """
        
        
        
    """
    Compute the standard deviation along the specified axis.

    Returns the standard deviation, a measure of the spread of a distribution,
    of the array elements. The standard deviation is computed for the
    flattened array by default, otherwise over the specified axis.

    Parameters
    ----------
    a : array_like
        Calculate the standard deviation of these values.
    axis : None or int or tuple of ints, optional
        Axis or axes along which the standard deviation is computed. The
        default is to compute the standard deviation of the flattened array.

        .. versionadded:: 1.7.0

        If this is a tuple of ints, a standard deviation is performed over
        multiple axes, instead of a single axis or all the axes as before.
    dtype : dtype, optional
        Type to use in computing the standard deviation. For arrays of
        integer type the default is float64, for arrays of float types it is
        the same as the array type.
    out : ndarray, optional
        Alternative output array in which to place the result. It must have
        the same shape as the expected output but the type (of the calculated
        values) will be cast if necessary.
    ddof : int, optional
        Means Delta Degrees of Freedom.  The divisor used in calculations
        is ``N - ddof``, where ``N`` represents the number of elements.
        By default `ddof` is zero.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

        If the default value is passed, then `keepdims` will not be
        passed through to the `std` method of sub-classes of
        `ndarray`, however any non-default value will be.  If the
        sub-class' method does not implement `keepdims` any
        exceptions will be raised.

    where : array_like of bool, optional
        Elements to include in the standard deviation.
        See `~numpy.ufunc.reduce` for details.

        .. versionadded:: 1.20.0

    Returns
    -------
    standard_deviation : ndarray, see dtype parameter above.
        If `out` is None, return a new array containing the standard deviation,
        otherwise return a reference to the output array.

    See Also
    --------
    var, mean, nanmean, nanstd, nanvar
    :ref:`ufuncs-output-type`

    Notes
    -----
    The standard deviation is the square root of the average of the squared
    deviations from the mean, i.e., ``std = sqrt(mean(x))``, where
    ``x = abs(a - a.mean())**2``.

    The average squared deviation is typically calculated as ``x.sum() / N``,
    where ``N = len(x)``. If, however, `ddof` is specified, the divisor
    ``N - ddof`` is used instead. In standard statistical practice, ``ddof=1``
    provides an unbiased estimator of the variance of the infinite population.
    ``ddof=0`` provides a maximum likelihood estimate of the variance for
    normally distributed variables. The standard deviation computed in this
    function is the square root of the estimated variance, so even with
    ``ddof=1``, it will not be an unbiased estimate of the standard deviation
    per se.

    Note that, for complex numbers, `std` takes the absolute
    value before squaring, so that the result is always real and nonnegative.

    For floating-point input, the *std* is computed using the same
    precision the input has. Depending on the input data, this can cause
    the results to be inaccurate, especially for float32 (see example below).
    Specifying a higher-accuracy accumulator using the `dtype` keyword can
    alleviate this issue.

    Examples
    --------
    >>> a = np.array([[1, 2], [3, 4]])
    >>> np.std(a)
    1.1180339887498949 # may vary
    >>> np.std(a, axis=0)
    array([1.,  1.])
    >>> np.std(a, axis=1)
    array([0.5,  0.5])

    In single precision, std() can be inaccurate:

    >>> a = np.zeros((2, 512*512), dtype=np.float32)
    >>> a[0, :] = 1.0
    >>> a[1, :] = 0.1
    >>> np.std(a)
    0.45000005

    Computing the standard deviation in float64 is more accurate:

    >>> np.std(a, dtype=np.float64)
    0.44999999925494177 # may vary

    Specifying a where argument:

    >>> a = np.array([[14, 8, 11, 10], [7, 9, 10, 11], [10, 15, 5, 10]])
    >>> np.std(a)
    2.614064523559687 # may vary
    >>> np.std(a, where=[[True], [True], [False]])
    2.0

    """