from modules.transformer import *
from modules.sim import *
from ltspice import Ltspice

class Reading:       
    def __init__(self, sim: Ltspice):
        self.sim = sim
    
    @staticmethod
    def _get_signal_type(expr: str) -> str:
        match = re.match(r'^([IV])\(', expr.strip())
        if not match:
            raise ValueError(f"Invalid signal expression: {expr}")
        signal_type = match.group(1)
        return 'A' if signal_type == 'I' else 'V'
    
    def _get_separate_signals(self, expr: str):
        # Match differential voltage: V(node1, node2)
        match_diff = re.match(r'V\(\s*([\w\d]+)\s*,\s*([\w\d]+)\s*\)', expr)
        if match_diff:
            pos_node, neg_node = match_diff.groups()
            return f"V({pos_node})", f"V({neg_node})"
        
        # Match single-ended voltage: V(node)
        match_single = re.match(r'V\(\s*([\w\d]+)\s*\)', expr)
        if match_single:
            pos_node = match_single.group(1)
            return f"V({pos_node})", None

        # If neither matches, it's an invalid format
        raise ValueError(f"Invalid voltage expression: {expr}")
    
    def get_data(self, signal: str):
        probe, reference = self._get_separate_signals(signal)
        p = self.sim.get_data(probe)
        
        if reference:
            p = self.sim.get_data(probe)
            r = self.sim.get_data(reference)
            
            diff = p - r
            
            return diff
        
        else:
            return p
        

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
        