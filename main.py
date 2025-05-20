from modules.transformer import *
from modules.spice import *
from modules.base_classes import *
import os
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt

raw_file_path_pc = r'C:\Users\eugene.dann\Documents\Development\circuit_development\circuit_sims\AM Circuits\Base Injected\Test AM curcuit\BaseInjectedAM.raw'
raw_file_path_mac = r'circuit_sims/AM Circuits/Base Injected/Test AM curcuit/BaseInjectedAM.raw'

sim_path = r'circuit_sims/AM Circuits/Base Injected/Test AM curcuit/BaseInjectedAM.raw'

circuit = Spice(sim_path)
circuit.parse()

carrier = circuit.get_data('V(n005, n003)')
time = circuit.get_time()

signals = []
signals.append(Signal(circuit, 'V(carrier)'))
signals.append(Signal(circuit, 'V(af)'))
signals.append(Signal(circuit, 'V(am)'))

fig, axs = plt.subplots(len(signals), 1, figsize=(10, 2.5 * len(signals)), sharex=True)
if len(signals) == 1:
    axs = [axs]

for ax, sig in zip(axs, signals):
    ax.plot(sig.time, sig.data, label=sig.name)
    ax.set_ylabel(f"{sig.name} [V]")  # Or whatever unit
    ax.legend(loc="upper right")
    ax.grid(True)

axs[-1].set_xlabel("Time [s]")

plt.tight_layout()
plt.show()




