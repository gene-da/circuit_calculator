from modules.transformer import *
from modules._sim import *
from ltspice import Ltspice
import re

class SpiceSim(Ltspice):       
    def __init__(self, path: str):
        super().__init__(path)
        
    @staticmethod
    def _get_signal_type(expr: str) -> str:
        match = re.match(r'^([IV])\(', expr.strip())
        if not match:
            raise ValueError(f"Invalid signal expression: {expr}")
        signal_type = match.group(1)
        return 'A' if signal_type == 'I' else 'V'

    def peak(self, signal_name: str, output: Output=Output.raw):
        signal_data = self.get_data(signal_name)
        
        if signal_data is None:
            raise ValueError(f"No data found for signal '{signal_name}'")
        
        reading = np.max(np.abs(signal_data))
        measurement_type = 'Peak'
        
        if output == Output.metric:
            return mn.to_metric(reading)
        
        elif output == Output.print:
            signal_type = self._get_signal_type(signal_name)
            value = mn.to_metric(reading, 2)
            print(f'{signal_name}: {value}{signal_type} {measurement_type}')
            
        elif output == Output.table:
            signal_type = self._get_signal_type(signal_name)
            value = mn.to_metric(reading, 2)
            return (signal_name, f'{value}{signal_type}', measurement_type)
            
        else:
            return reading

    def peak_to_peak(self, signal_name: str, output: Output=Output.raw):
        signal_data = self.sim.get_data(signal_name)
        
        if signal_data is None:
            raise ValueError(f"No data found for signal '{signal_name}'")
        
        reading = np.max(signal_data) -  np.min(signal_data)
        measurement_type = 'Peak to Peak'
        
        if output == Output.metric:
            return mn.to_metric(reading)
        
        elif output == Output.print:
            signal_type = self._get_signal_type(signal_name)
            value = mn.to_metric(reading, 2)
            print(f'{signal_name}: {value}{signal_type} {measurement_type}')
            
        elif output == Output.table:
            signal_type = self._get_signal_type(signal_name)
            value = mn.to_metric(reading, 2)
            return (signal_name, f'{value}{signal_type}', measurement_type)
            
        else:
            return reading

    def true_rms(self, signal_name: str, output: Output=Output.raw):
        signal_data = self.sim.get_data(signal_name)
        
        if signal_data is None:
            raise ValueError(f"No data found for signal '{signal_name}'")
        
        reading = np.sqrt(np.mean(signal_data**2))
        measurement_type = 'True RMS'
        
        if output == Output.metric:
            return mn.to_metric(reading)
        
        elif output == Output.print:
            signal_type = self._get_signal_type(signal_name)
            value = mn.to_metric(reading, 2)
            print(f'{signal_name}: {value}{signal_type} {measurement_type}')
            
        elif output == Output.table:
            signal_type = self._get_signal_type(signal_name)
            value = mn.to_metric(reading, 2)
            return (signal_name, f'{value}{signal_type}', measurement_type)
            
        else:
            return reading
        
    def peak_to_peak_rms(self, signal_name: str, output: Output=Output.raw):
        signal_data = self.sim.get_data(signal_name)
        
        if signal_data is None:
            raise ValueError(f"No data found for signal '{signal_name}'")
        
        peak_peak = np.max(signal_data) -  np.min(signal_data)
        reading = peak_peak / (2 * np.sqrt(2))
        measurement_type = 'Peak to Peak RMS'
        
        if output == Output.metric:
            return mn.to_metric(reading)
        
        elif output == Output.print:
            signal_type = self._get_signal_type(signal_name)
            value = mn.to_metric(reading, 2)
            print(f'{signal_name}: {value}{signal_type} {measurement_type}')
            
        elif output == Output.table:
            signal_type = self._get_signal_type(signal_name)
            value = mn.to_metric(reading, 2)
            return (signal_name, f'{value}{signal_type}', measurement_type)
            
        else:
            return reading

    def peak_rms(self, signal_name: str, output: Output=Output.raw):
        signal_data = self.sim.get_data(signal_name)
        
        if signal_data is None:
            raise ValueError(f"No data found for signal '{signal_name}'")
        
        peak = np.max(np.abs(signal_data))
        reading = peak / (np.sqrt(2))
        measurement_type = 'Peak RMS'
        
        if output == Output.metric:
            return mn.to_metric(reading)
        
        elif output == Output.print:
            signal_type = self._get_signal_type(signal_name)
            value = mn.to_metric(reading, 2)
            print(f'{signal_name}: {value}{signal_type} {measurement_type}')
            
        elif output == Output.table:
            signal_type = self._get_signal_type(signal_name)
            value = mn.to_metric(reading, 2)
            return (signal_name, f'{value}{signal_type}', measurement_type)
            
        else:
            return reading

    def average(self, signal_name: str, output: Output=Output.raw):
        signal_data = self.sim.get_data(signal_name)
        
        if signal_data is None:
            raise ValueError(f"No data found for signal '{signal_name}'")
        
        reading = np.mean(signal_data)
        measurement_type = 'Average'
        
        if output == Output.metric:
            return mn.to_metric(reading)
        
        elif output == Output.print:
            signal_type = self._get_signal_type(signal_name)
            value = mn.to_metric(reading, 2)
            print(f'{signal_name}: {value}{signal_type} {measurement_type}')
            
        elif output == Output.table:
            signal_type = self._get_signal_type(signal_name)
            value = mn.to_metric(reading, 2)
            return (signal_name, f'{value}{signal_type}', measurement_type)
            
        else:
            return reading
        