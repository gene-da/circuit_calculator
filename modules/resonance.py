import numpy as np
from modules import metric_notation as mn
from modules import reactance as react
from modules.constants import *

class LCTank:
    def __init__(self, inductance, capacitance):
        self.inductance = mn.from_metric(inductance)
        self.capacitance = mn.from_metric(capacitance)

    def frequency(self, metric=False):
        if metric:
            return Resonance.frequncy_from_l_c(self.inductance, self.capacitance, True)
        else:
            return Resonance.frequncy_from_l_c(self.inductance, self.capacitance)

    def print_frequency(self):
        cap = mn.to_metric(self.capacitance, 1)
        ind = mn.to_metric(self.inductance, 1)
        print(f'Resonant Frequency: {self.frequency(metric=True)}Hz (From: {cap}F {ind}H)')

    def inductive_reactance(self, target_frequency, metric=False):
        frequency = mn.from_metric(target_frequency)
        reactance = react.Inductance.reactance(frequency, self.inductance)

        if metric:
            return mn.to_metric(reactance, 2)
        else:
            return reactance

    def print_inductive_reactance(self, target_frequency):
        frequency = mn.from_metric(target_frequency)
        reactance = self.inductive_reactance(frequency, True)
        adj_capacitance = Resonance.capacitance_from_l_f(self.inductance, frequency, True)

        print(f'Frequency: {target_frequency}Hz Inductance: {mn.to_metric(self.inductance, 2)}H Reactance: {reactance}{omega}')
        print(f'Adjust Capacitance: {adj_capacitance}F')


class Resonance:
    @staticmethod
    def frequncy_from_l_c(inductance, capacitance, metric=False):
        l = mn.from_metric(inductance)
        c = mn.from_metric(capacitance)
        freq = 1 / (2 * np.pi * np.sqrt(l * c))

        if metric:
            return mn.to_metric(freq, 2)
        else:
            return freq

    @staticmethod
    def capacitance_from_l_f(inductance, frequency, metric=False):
        l = mn.from_metric(inductance)
        f = mn.from_metric(frequency)

        capacitance = 1 / (4 * np.power(np.pi, 2) * np.power(f, 2) * l)
        if metric:
            return mn.to_metric(capacitance, 2)
        else:
            return capacitance