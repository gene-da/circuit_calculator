from modules.transformer import *
from modules.sim import *
from modules.reading import Reading
from modules.base_classes import *
import os
from tabulate import tabulate


raw_file_path = r'C:\Users\eugene.dann\Documents\Development\circuit_development\circuit_sims\AM Circuits\Base Injected\Test AM curcuit\BaseInjectedAM.raw'

def print_reading_table(readings: list[tuple[str, str, str]]):
    print(f"{'Signal':<15} {'Value':<12} {'Type':<15}")
    print("-" * 42)
    for signal, value, rtype in readings:
        print(f"{signal:<15} {value:<12} {rtype:<15}")

class Read:
    class DMM(Enum):
        AC = auto()
        DC = auto()
    
    class Oscope:
        class Coupling(Enum):
            AC = auto()
            DC = auto()
    
    class Raw(Enum):
        peak        = auto()
        pkpk        = auto()
        true_rms    = auto()
        pk_rms      = auto()
        pkpk_rms    = auto()
        average     = auto()

    
class Sim(Reading):
    def __init__(self, sim_data_path):
        sim = ltspice.Ltspice(sim_data_path)
        sim.parse()
        
        super().__init__(sim)
        
        self.results = []
        
    def probe(self, signal: str, type: Read, output: Output=Output.print):
        if type == Read.DMM.AC or type == Read.Raw.pkpk_rms:
            print('DMM AC')
            return self.peak_to_peak_rms(signal, output)
            
        elif type == Read.DMM.DC or type == Read.Raw.peak:
            print('DMM DC')
            return self.peak(signal, output)
        
        elif type == Read.Oscope.Coupling.AC or type == Read.Raw.pkpk:
            print('Oscope Coupling AC')
            return self.peak_to_peak(signal, output)
        
        elif type == Read.Oscope.Coupling.DC or type == Read.Raw.average:
            print('Oscope Coupling DC')
            return self.peak_rms(signal, output)

read = Sim(raw_file_path)

results = []

read.peak('V(n003, n005)', Output.print)

read.probe('V(n003)', Read.Oscope.Coupling.AC)



