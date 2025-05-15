from modules.transformer import *
from modules.sim import *
from ltspice import Ltspice

raw_file_path = r'C:\Users\eugene.dann\Documents\Development\circuit_development\circuit_sims\AM Circuits\Base Injected\Test AM curcuit\BaseInjectedAM.raw'
data = get_sim_data(raw_file_path)

def test_function(sim_data: Ltspice, signal: str):
    data = sim_data.get_data(signal)
    
    print()
    print(f'{signal}')
    peak = np.max(np.abs(data))
    print(f'Peak Voltage: {mn.to_metric(peak)}V')
    
    peak_peak = np.max(data) -  np.min(data)
    print(f'Peak to Peak Voltage: {mn.to_metric(peak_peak)}V')
    
    rms_mean = np.sqrt(np.mean(data**2))
    print(f'True RMS Voltage: {mn.to_metric(rms_mean)}V')
    
    rms_pp = peak_peak / (2 * np.sqrt(2))
    print(f'RMS Voltage (PEAK TO PEAK): {mn.to_metric(rms_pp)}V')
    
    rms_peak = peak / (np.sqrt(2))
    print(f'RMS Voltage (PEAK): {mn.to_metric(rms_peak)}V')
    
    mean = np.mean(data)
    print(f'Average Voltage: {mn.to_metric(mean)}V')

class Measurment(Enum):
    pk      = auto()
    pkpk    = auto()
    tr_rms  = auto()
    pp_rms  = auto()
    pk_rms  = auto()
    avg     = auto()

class Reading:   
    class Type(Enum):
        pk      = auto()
        pkpk    = auto()
        tr_rms  = auto()
        pp_rms  = auto()
        pk_rms  = auto()
        avg     = auto()
    
    @staticmethod
    def get_signal_type(expr: str) -> str:
        match = re.match(r'^([IV])\(', expr.strip())
        if not match:
            raise ValueError(f"Invalid signal expression: {expr}")
        return match.group(1)
        
    @staticmethod
    def peak(signal_data, signal_name: str, output: Output=Output.raw):
        reading = np.max(np.abs(signal_data))
        
        if output == Output.metric:
            return mn.to_metric(reading)
        
        elif output == Output.print:
            if Reading.get_signal_type(signal_name) == 'I':
                print(f'Reading {signal_name}: {mn.to_metric(reading)}Apk')
                return mn.to_metric(reading)
            
            elif Reading.get_signal_type(signal_name) == 'V':
                print(f'Reading {signal_name}: {mn.to_metric(reading)}Vpk')
                return mn.to_metric(reading)
            
            else:
                raise ValueError(f'READING TYPE NOT HANDLED: {Reading.get_signal_type(signal_name)}')
            
        else:
            return reading
        
    @staticmethod
    def peak_to_peak(sim_data: Ltspice, signal: str):
        data = sim_data.get_data(signal)
        
    @staticmethod
    def true_rms(sim_data: Ltspice, signal: str):
        data = sim_data.get_data(signal)
        
    @staticmethod
    def peak_to_peak_rms(sim_data: Ltspice, signal: str):
        data = sim_data.get_data(signal)
        
    @staticmethod
    def peak_rms(sim_data: Ltspice, signal: str):
        data = sim_data.get_data(signal)
        
    @staticmethod
    def average(sim_data: Ltspice, signal: str):
        data = sim_data.get_data(signal)
    

    
def differential(sim: Ltspice, probe: str, reference: str):
    p = sim.get_data(probe)
    r = sim.get_data(reference)
    
    diff = p - r
    
    return diff
    
def get_reading(sim: Ltspice, measurment: str, reading_type: Reading):
    probe, reference = get_separate_signals(measurment)
    
    if reference:
        data = differential(sim, probe, reference)
        peak = np.max(np.abs(data))
        print(f'Peak Voltage: {mn.to_metric(peak)}V')
        
    else:
        print(f'Nothing in reference')
        

Reading.peak(data.get_data('V(carrier)'), 'V(carrier)', Output.print)
Reading.peak(data.get_data('I(L3)'), 'I(L3)', Output.print)