"""
This is an activation of a neuron it contains a pointer to a neuron as well as the time it activated
"""


class Activation:
    def __init__(self, neuron, time):
        self._neuron = neuron
        self._time = time

    @property
    def neuron(self):
        return self._neuron

    @property
    def time(self):
        return self._time
