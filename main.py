from modules import reactance
from modules.constants import *
from modules.resonance import LCTank

C1 = '68n'
L1 = '47u'
R1 = '33'
f = '1k'

tank = LCTank(L1, C1)

reactance_raw = reactance.Capacitive.reactance(f, C1)
reactance_metric = reactance.Capacitive.reactance(f, C1, True)
frequency = reactance.Capacitive.frequency(reactance_raw, C1, True)
capacitance = reactance.Capacitive.capacitance(reactance_raw, frequency, True)

print(f'X (raw): {reactance_raw}{omega}')
print(f'X (metric): {reactance_metric}{omega}')
print(f'frequency: {frequency}{omega}')
print(f'Resonant Frequency: {tank.frequency(metric=True)}Hz (From: {C1}F {L1}H)')
tank.print_frequency()

tank.print_inductive_reactance(tank.frequency()) #this now