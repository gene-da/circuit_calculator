from __future__ import annotations
import os
from pathlib import Path
import platform
from typing import List, Union
import numpy as np
import re
from . import metric_notation as mn
from . import plt_theme as plot
import matplotlib.pyplot as plt

if list(map(lambda x: int(x), platform.python_version_tuple())) >= [3, 8, 0]:
    from typing import Literal
else:
    from typing_extensions import Literal

from deprecated import deprecated

class LtspiceException(Exception):
    pass
class VariableNotFoundException(LtspiceException):
    pass
class FileSizeNotMatchException(LtspiceException):
    pass
class InvalidPhysicalValueRequestedException(LtspiceException):
    pass
class UnknownEncodingTypeException(LtspiceException):
    pass

import matplotlib.pyplot as plt

def plot_signals(signals, metric_type):
    plt.rcParams.update(plot.theme)
    fig, axs = plt.subplots(len(signals), 1, figsize=(15, 3 * len(signals)), sharex=True)

    if len(signals) == 1:
        axs = [axs]

    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    for idx, (ax, sig) in enumerate(zip(axs, signals)):
        color = color_cycle[idx % len(color_cycle)]  # Cycle if too many signals
        line, = ax.plot(sig.time, sig.data, color=color)

        # Get the metric
        metric = sig.read(metric_type)

        # Format safely
        if isinstance(metric, (int, float)):
            legend_label = f"{sig.name}\n{metric:.3f} V"
        elif isinstance(metric, str):
            legend_label = f"{sig.name}\n{metric}"
        else:
            legend_label = f"{sig.name}\nN/A"

        ax.set_xlim(sig.time[0], sig.time[-1])
        ax.legend([line], [legend_label], loc="upper right")
        ax.set_ylabel(f"{sig.name} [V]", color=color)
        ax.tick_params(axis='y', colors=color)
        ax.grid(True)

    axs[-1].set_xlabel("Time [s]")
    plt.tight_layout()
    fig.subplots_adjust(
        left=0.01,
        right=0.98,
        top=0.98,
        bottom=0.05,
        hspace=0.00
    )

    plt.show()



class Signal:
    def __init__(self, sim, signal_name: str):
        self.name = signal_name
        self.data = sim.get_data(signal_name)
        self.time = sim.get_time()

        if self.data is None:
            raise ValueError(f"Signal '{signal_name}' not found in simulation data.")

        if len(self.data) != len(self.time):
            raise ValueError(f"Signal '{signal_name}' data length does not match time vector.")

    def __repr__(self):
        return f"<Signal name='{self.name}' samples={len(self.data)}>"

    def read(self, type: str):
        import re
        match = re.match(r'^([IV])\(', self.name.strip())
        if not match:
            raise ValueError(f"Invalid signal expression: {self.name}")
        
        meas_type = 'A' if match.group(1) == 'I' else 'V'

        if type == 'peak':
            peak = (np.max(self.data) - np.min(self.data)) / 2
            return f'{mn.to_metric(peak)}{meas_type}pk'

    def plot(self, metric_type: str, coupling: str = 'DC'):
        import matplotlib.pyplot as plt
        plt.rcParams.update(plot.theme)

        fig, ax = plt.subplots(figsize=(15, 3))

        # Plot the signal
        line, = ax.plot(self.time, self.data)

        # Read and format metric
        metric = self.read(metric_type)
        if isinstance(metric, (int, float)):
            legend_label = f"{self.name}\n{metric:.3f} V"
        elif isinstance(metric, str):
            legend_label = f"{self.name}\n{metric}"
        else:
            legend_label = f"{self.name}\nN/A"

        # Set X limits
        ax.set_xlim(self.time[0], self.time[-1])

        # 👉 Coupling-specific Y-axis adjustment
        if coupling.upper() == 'DC':
            sig_min = self.data.min()
            sig_max = self.data.max()

            if sig_min > 0:
                ymin = 0
            elif sig_max < 0:
                ymin = 0
            else:
                # If it crosses zero, set lower limit to whichever is closer to zero
                ymin = sig_min if abs(sig_min) < abs(sig_max) else sig_max

            ax.set_ylim(bottom=ymin)  # Leave top limit auto-scaled

        # AC: no Y-limit adjustments
        ax.legend([line], [legend_label], loc="upper right")
        ax.set_ylabel(f"{self.name} [V]")
        ax.set_xlabel("Time [s]")
        ax.grid(True)

        fig.subplots_adjust(left=0.01, right=0.98, top=0.98, bottom=0.10)
        plt.tight_layout()
        plt.show()


class Spice:
    max_header_size : int = int(1e6)
    def __init__(self, file_path : Union[str, Path],
        mode      :Literal['Transient', 'FFT', 'AC', 'DC', 'Noise', 'Operating Point'] = 'Transient',
        file_type :Literal['Binary', 'Ascii'] = "Binary",
        x_dtype : Union[np.float32, np.float64, np.complex128] = np.float64,
        y_dtype : Union[np.float32, np.float64, np.complex128] = np.float32, 
        encoding: Literal['utf-16-le', 'utf8', 'unknown'] = 'unknown'):
        
        self.file_path = file_path
        self.dsamp : int = 1
        self.tags  : List[str]= ['Title:', 'Date:', 'Plotname:', 'Flags:', 'No. Variables:', 'No. Points:', 'Offset:']
        self.x_raw = []
        self.y_raw = []
        self._case_split_point = []

        #TODO : refactor header to another struct
        self.title = ''
        self.date = ''
        self.plot_name = ''
        self.flags = []
        self.offset = 0
        
        self._point_num :int       = 0   # all point number
        self._variables :List[str] = []  # variable list
        self._types     :List[str] = []  # type list
        self._mode       = mode 
        self._file_type  = file_type
        self._x_dtype    = x_dtype
        self._y_dtype    = y_dtype
        self._encoding   = encoding

        self.header_size = 0
        self.read_header()

    def set_variable_dtype(self, t)->Spice:
        self._y_dtype = t
        return self

    def read_header(self)->None:
        filesize = os.stat(self.file_path).st_size
        
        # if the file is too big, read only the designated amount of bytes
        with open(self.file_path, 'rb') as f:
            if filesize > self.max_header_size:
                data = f.read(self.max_header_size)  
            else:
                data = f.read()  

        #TODO : have to find more adequate way to determine proper encoding of text..
        try:
            buffer_line = ''
            header_content_lines = []   
            byte_index_line_begin = 0
            byte_index_line_end = 0
            try:
                while not ('Binary' in buffer_line or 'Values' in buffer_line):
                    if bytes([data[byte_index_line_end]]) == b'\n':
                        buffer_line = str(bytes(data[byte_index_line_begin:byte_index_line_end+2]), encoding='UTF16')
                        header_content_lines.append(buffer_line)
                        byte_index_line_begin = byte_index_line_end+2
                        byte_index_line_end   = byte_index_line_begin
                    else:
                        byte_index_line_end += 1
                self._encoding = 'utf-16-le'
            except IndexError as e:
                print("Variable description header size is over 1Mbyte. Please adjust max_header_size manually.")
                raise e
        except UnicodeDecodeError as e:
            buffer_line = ''
            header_content_lines = []   
            byte_index_line_begin = 0
            byte_index_line_end = 0
            try:
                while not ('Binary' in buffer_line or 'Values' in buffer_line):
                    if bytes([data[byte_index_line_end]]) == b'\n':
                        buffer_line = str(bytes(data[byte_index_line_begin:byte_index_line_end+1]), encoding='UTF8')
                        header_content_lines.append(buffer_line)
                        byte_index_line_begin = byte_index_line_end+1
                        byte_index_line_end   = byte_index_line_begin
                    else:
                        byte_index_line_end += 1
                self._encoding = 'utf-8'
            except IndexError as e:
                print("Variable description header size is over 1Mbyte. Please adjust max_header_size manually.")
                raise e

        if self._encoding == 'unknown':
            raise UnknownEncodingTypeException("Unknown encoding type")

        header_content_lines = [x.rstrip().rstrip() for x in header_content_lines]

        # remove string header from binary data 
        self.header_size = byte_index_line_end

        variable_declaration_line_num = header_content_lines.index('Variables:')
        header_content_only_lines     = header_content_lines[0:variable_declaration_line_num]
        variable_type_content_lines   = header_content_lines[variable_declaration_line_num+1:-1]

        for header_content_line in header_content_only_lines:
            if self.tags[0] in header_content_line:
                self.title = header_content_line[len(self.tags[0]):]
            if self.tags[1] in header_content_line:
                self.date = header_content_line[len(self.tags[1]):]
            if self.tags[2] in header_content_line:
                self.plot_name = header_content_line[len(self.tags[2]):]
            if self.tags[3] in header_content_line:
                self.flags = header_content_line[len(self.tags[3]):].split(' ')
            if self.tags[4] in header_content_line:
                self._variable_num = int(header_content_line[len(self.tags[4]):])
            if self.tags[5] in header_content_line:
                self._point_num = int(header_content_line[len(self.tags[5]):])
            if self.tags[6] in header_content_line:
                self.offset = float(header_content_line[len(self.tags[6]):])

        for variable_type_content_line in variable_type_content_lines:
            variable_type_split_list = variable_type_content_line.split()
            self._variables.append(variable_type_split_list[1])
            self._types.append(variable_type_split_list[2])

        # check mode
        if 'FFT' in self.plot_name:
            self._mode = 'FFT'
        elif 'Transient' in self.plot_name:
            self._mode = 'Transient'
        elif 'AC' in self.plot_name:
            self._mode = 'AC'
        elif 'DC' in self.plot_name:
            self._mode = 'DC'
        elif 'Noise' in self.plot_name:
            self._mode = 'Noise'
        elif 'Operating Point' in self.plot_name:
            self._mode = "Operating Point"

        # check file type
        if 'Binary' in header_content_lines[-1]:
            self._file_type = 'Binary'

            if 'double' in self.flags:
                self._y_dtype = np.float64

        elif 'Value' in header_content_lines[-1]:
            self._file_type = 'Ascii'
            self._y_dtype = np.float64
        else:
            raise UnknownEncodingTypeException

        if self._mode == 'FFT' or self._mode == 'AC':
            self._y_dtype = np.complex128
            self._x_dtype = np.complex128
        
    
    def parse(self):
        if self._file_type == 'Binary':
            #Check data size
            variable_data_size = np.dtype(self._y_dtype).itemsize  
            time_data_size     = np.dtype(self._x_dtype).itemsize  
            diff = int(( time_data_size - variable_data_size ) / variable_data_size)

            variable_data_len  = self._point_num * (self._variable_num - 1) * variable_data_size
            time_data_len      = self._point_num * time_data_size
            expected_data_len  = variable_data_len + time_data_len

            with open(self.file_path, 'rb') as f:
                data = f.read()[self.header_size:]
            
            if not len(data) == expected_data_len:
                if len(data) == variable_data_len * 2 + time_data_len:
                    print("[Warning] Variable data type is detected as double precision.")
                    self._y_dtype = np.float64
                else:
                    raise FileSizeNotMatchException

            if self._y_dtype == self._x_dtype:
                self._y_dtype = self._x_dtype
                self.y_raw = np.frombuffer(data, dtype=self._y_dtype)
                self.x_raw = self.y_raw[::self._variable_num]
                self.y_raw = np.reshape(self.y_raw, (self._point_num, self._variable_num))
            else:
                self.y_raw = np.frombuffer(data, dtype=self._y_dtype)
                self.x_raw = np.zeros(self._point_num, dtype=self._x_dtype)
                for i in range(self._point_num):
                    d = data[
                            i * (self._variable_num + diff) * variable_data_size:
                            i * (self._variable_num + diff) * variable_data_size + time_data_size
                        ]
                        
                    self.x_raw[i] = np.frombuffer(d, dtype=self._x_dtype)

                self.y_raw = np.reshape(np.array(self.y_raw), (self._point_num, self._variable_num + diff))
                self.y_raw = self.y_raw[:, diff:]
                self.y_raw[:,0] = self.x_raw
            
            if self._mode == "Transient" or self._mode == "AC" or self._mode == "FFT":
                self.x_raw = np.abs(self.x_raw)
                
        elif self._file_type == 'Ascii':
            with open(self.file_path, 'r', encoding=self._encoding) as f:
                data = f.readlines()
            data = [x.rstrip() for x in data]
            data = data[data.index('Values:') + 1:]

            if self._y_dtype == np.float64 or self._y_dtype == np.float32:
                self.y_raw = np.array([self._y_dtype(
                    x.split('\t')[-1]
                    ) for  x  in data]).reshape((self._point_num, self._variable_num))
                pass

            if self._y_dtype == np.complex128 or self._y_dtype == np.complex64:
                data = list(filter(lambda x : len(x) > 0 , data))
                self.y_raw = np.array([self._y_dtype(
                    complex(*[float(y) for y in x.split('\t', 1)[-1].split(',')])
                    ) for  x  in data]).reshape((self._point_num, self._variable_num))
                pass

            self.x_raw = self.y_raw[:,0]
            pass
              
        # Split cases
        self._case_split_point.append(0)

        start_value = self.x_raw[0]

        for i in range(self._point_num - 1):
            if self.x_raw[i + 1] == start_value:
                self._case_split_point.append(i + 1)
        self._case_split_point.append(self._point_num)
        return self

    def get_data(self, name, case=0, time=None, frequency=None):
        # Handle differential signals like V(n003, n005)
        if ',' in name:
            # Strip whitespace and filter out garbage from re.split
            variable_names = [v.strip() for v in re.split(r',|\(|\)', name) if v.strip()]
            
            # Sanity check: make sure we have at least two nodes after V
            if len(variable_names) < 3:
                raise ValueError(f"Invalid differential signal format: {name}")
            
            # Extract individual node voltages
            data1 = self.get_data(f'V({variable_names[1]})', case, time)
            data2 = self.get_data(f'V({variable_names[2]})', case, time)

            if data1 is None or data2 is None:
                raise ValueError(f"Signal(s) missing in .raw file: {variable_names[1]} or {variable_names[2]}")

            return data1 - data2

        else:
            # Case-insensitive match against available variables
            variables_lowered = [v.lower() for v in self._variables]

            if name.lower() not in variables_lowered:
                return None

            variable_index = variables_lowered.index(name.lower())
            data = self.y_raw[self._case_split_point[case]:self._case_split_point[case + 1], variable_index]

            # Return full waveform or interpolate based on time/frequency
            if time is None and frequency is None:
                return data
            elif time is not None:
                return np.interp(time, self.get_time(case), data)
            elif frequency is not None:
                return np.interp(frequency, self.get_frequency(case), data)
            else:
                return None
 

    def get_x(self, case=0):
        return self.x_raw[self._case_split_point[case]:self._case_split_point[case + 1]]
    
    def get_time(self, case=0):
        if self._mode == 'Transient' or self._mode == 'DC':
            return self.get_x(case = case)
        else:
            raise InvalidPhysicalValueRequestedException

    def get_frequency(self, case=0):
        if self._mode == 'FFT' or self._mode == 'AC' or self._mode == 'Noise':
            return np.abs(self.get_x(case = case))
        else:
            raise InvalidPhysicalValueRequestedException

    @property
    def variables(self):
        return self._variables

    @property
    def time(self):
        return self.get_time(case=0)

    @property
    def frequency(self):
        return self.get_frequency(case=0)

    @property
    def case_count(self):
        return len(self._case_split_point) - 1

    @deprecated(version='1.0.0', reason="use method which follows pep8")
    def getData(self, name, case=0, time=None):
        return self.get_data(name, case, time)

    @deprecated(version='1.0.0', reason="use method which follows pep8")
    def getTime(self,case=0):
        return self.get_time(case)

    @deprecated(version='1.0.0', reason="use method which follows pep8")
    def getFrequency(self, case=0):
        return self.get_frequency(case)

    @deprecated(version='1.0.0', reason="use method which follows pep8")
    def getVariableNames(self, case=0):
        return self._variables

    @deprecated(version='1.0.0', reason="use method which follows pep8")
    def getVariableTypes(self, case=0):
        return self._types

    @deprecated(version='1.0.0', reason="use method which follows pep8")
    def getCaseNumber(self):
        return len(self._case_split_point)

    @deprecated(version='1.0.0', reason="use method which follows pep8")
    def getVariableNumber(self):
        return len(self._variables)
    
