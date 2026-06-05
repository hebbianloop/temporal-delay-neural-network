"""
This is the Masquelier 2008 delay function.
"""

import math
from .function_super import DelayFunction


class Masq(DelayFunction):
    def __init__(self, input_, options, variable):
        super().__init__(input_, options)
        self._weight = variable.value

    def update_value(self):
        self._time += self._options['network_speed']
        _mem_tc = 10  # value from Masquelier 2008
        _syn_tc = 2.5  # value from Masquelier 2008
        _constant = 2.11653473596  # calculated to make max value of function 1
        _scale_time = (self._time * 70) / self._end_time
        self._value = self._weight * _constant * (math.exp(-_scale_time / _mem_tc) - math.exp(-_scale_time / _syn_tc))
        return self
