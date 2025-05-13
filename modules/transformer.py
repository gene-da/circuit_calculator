import numpy as np
from enum import Enum, auto
from modules.constants import *
from modules import metric_notation as mn
from modules import reactance as react

class CoilType(Enum):
    inductor = auto()
    winds = auto()
    
class Transformer:
    def __init__(self, primary, secondary, coil: CoilType):
        self.primary = mn.from_metric(primary)
        self.secondaey = mn.from_metric(secondary)
        self.coil = coil
        

def turns_ratio(coil: CoilType, primary_winding, secondary_winding, output: Output=Output.raw):        
    
    n1 = mn.from_metric(primary_winding)
    n2 = mn.from_metric(secondary_winding)
    
    
    if coil == CoilType.winds:
        a = n1 / n2
        if output == Output.metric:
            return mn.to_metric(a, 2)

        elif output == Output.print:
            print()
            print(f'Primary Turns: {n1}')
            print(f'Secondary Turns: {n2}')
            print(f'Turns Ratio: {a}')
            return a

        else:
            return a
        
    elif coil == CoilType.inductor:
        a = np.sqrt( n1 / n2 )
        if output == Output.metric:
            return mn.to_metric(a, 2)

        elif output == Output.print:
            print()
            print(f'Primary Inductance: {mn.to_metric(n1, 2)}H')
            print(f'Secondary Inductance: {mn.to_metric(n2, 2)}H')
            print(f'Turns Ratio: {a}')
            return a

        else:
            return a
        
    
def voltage_transformation(winding: Winding, ratio, voltage, output: Output=Output.raw):
    a = mn.from_metric(ratio)
    v = mn.from_metric(voltage)
    
    if winding == Winding.primary:
        return_voltage = a * v
        
        if output == Output.metric:
            return mn.to_metric(return_voltage, 2)
        
        elif output == Output.print:
            print()
            print(f'Winding Ratio: {ratio}')
            print(f'Secondary Winding Votlage: {mn.to_metric(v, 2)}V')
            print(f'Primary Winding Voltage: {mn.to_metric(return_voltage, 2)}V')
            print()
            
            return return_voltage
        
        else:
            return return_voltage
        
    elif winding == Winding.secondary:
        return_voltage = v / a
        
        if output == Output.metric:
            return mn.to_metric(return_voltage, 2)
        
        elif output == Output.print:
            print()
            print(f'Winding Ratio: {ratio}')
            print(f'Primary Winding Votlage: {mn.to_metric(v, 2)}V')
            print(f'Secondary Winding Voltage: {mn.to_metric(return_voltage, 2)}V')
            print()
            
            return return_voltage
        
        else:
            return return_voltage
        
    else:
        print(f'Unhandled object: {winding}')
        

    