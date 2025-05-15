import numpy as np
from modules import metric_notation as mn


class Capacitive:
    @staticmethod
    def reactance(frequency, capacitance, metric=True):
        c = mn.from_metric(capacitance)
        w = 2 * np.pi * mn.from_metric(frequency)
        reactance = 1 / (w * c)
        if metric:
            return mn.to_metric(reactance, 2)
        else:
            return reactance

    @staticmethod
    def capacitance(frequency, reactance, metric=False):
        l = mn.from_metric(reactance)
        w = 2 * np.pi * mn.from_metric(frequency)
        capacitance = w * l
        if metric:
            return mn.to_metric(capacitance, 2)
        else:
            return capacitance

    @staticmethod
    def frequency(reactance, capacitance, metric=False):
        c = mn.from_metric(capacitance)
        z = mn.from_metric(reactance)
        freq = 1 / (2 * np.pi * c * z)

        if metric:
            return mn.to_metric(freq, 2)
        else:
            return freq

class Inductance:
    @staticmethod
    def reactance(frequency, inductance, metric=False):
        l = mn.from_metric(inductance)
        w = 2 * np.pi * mn.from_metric(frequency)
        reactance = w * l

        if metric:
            return mn.to_metric(reactance, 2)
        else:
            return reactance

    @staticmethod
    def inductance(frequency, reactance, metric=False):
        x = mn.from_metric(reactance)
        w = 2 * np.pi * mn.from_metric(frequency)
        inductance = x / w

        if metric:
            return mn.to_metric(inductance, 2)
        else:
            return inductance

    @staticmethod
    def frequency(reactance, inductance, metric=False):
        l = mn.from_metric(inductance)
        x = mn.from_metric(reactance)
        freq = x / (2 * np.pi * l)

        if metric:
            return mn.to_metric(freq, 2)
        else:
            return freq