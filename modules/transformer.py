import numpy as np
from enum import Enum, auto
from modules.constants import *
from modules import metric_notation as mn
from modules import reactance as react
    
class Transformer:
    def __init__(self, primary, secondary, coil: CoilType):
        self.primary = mn.from_metric(primary)
        self.secondaey = mn.from_metric(secondary)
        self.coil = coil
        
def secondary_load(secondary_impedenace, secondary_inductance, frequency):
    f = mn.from_metric(frequency)
    l = mn.from_metric(secondary_inductance)
    z = mn.from_metric(secondary_impedenace)
    x = 2 * np.pi * f * l
    r = abs(z**2 - x**2)
    if r < 0:
        raise ValueError("Invalid value: R^2 is NEGATIVE")
    
    return abs(r)

def turns_ratio_inductance(primary, secondary):
    n1 = mn.from_metric(primary)
    n2 = mn.from_metric(secondary)
    
    return np.sqrt(n1 / n2)

def turns_ratio_windings(primary, secondary):
    n1 = mn.from_metric(primary)
    n2 = mn.from_metric(secondary)
    
    return n1 / n2

def turns_ratio(coil: CoilType, primary_coil, secondary_coil, output: Output=Output.raw):
    if coil == CoilType.windings:
        a = turns_ratio_windings(primary_coil, secondary_coil)
        if output == Output.metric:
            return mn.to_metric(a, 2)

        elif output == Output.print:
            n1 = mn.to_metric(mn.from_metric(primary_coil), 2)
            n2 = mn.to_metric(mn.from_metric(secondary_coil), 2)
            print()
            print(f'Primary Turns: {n1}')
            print(f'Secondary Turns: {n2}')
            print(f'Turns Ratio: {a}')
            return a

        else:
            return a
        
    elif coil == CoilType.inductor:
        a = turns_ratio_inductance(primary_coil, secondary_coil)
        if output == Output.metric:
            return mn.to_metric(a, 2)

        elif output == Output.print:
            n1 = mn.to_metric(mn.from_metric(primary_coil))
            n2 = mn.to_metric(mn.from_metric(secondary_coil))
            print()
            print(f'Primary Inductance: {n1}H')
            print(f'Secondary Inductance: {n2}H')
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
        

    