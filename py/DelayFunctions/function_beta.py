"""
This is the beta delay function.
"""

import math
from .function_super import DelayFunction


class Beta(DelayFunction):
    def __init__(self, input_, options, variable):
        super().__init__(input_, options)
        self._alpha = variable.value['alpha']
        self._beta = variable.value['beta']

    def update_value(self):
        self._time += self._options['network_speed']
        _beta_func = math.exp(
            math.lgamma(self._alpha + self._beta) - (math.lgamma(self._alpha) + math.lgamma(self._beta)))
        _scale_time = self._time / self._end_time
        if _scale_time == 0 or _scale_time == 1:
            self._value = 0
        else:
            self._value = (((1 - _scale_time) ** (self._beta - 1)) * _scale_time ** (self._alpha - 1)) * _beta_func
        return self

    def update_weights(self, item):
        self._alpha = item.value['alpha']
        self._beta = item.value['beta']

    @property
    def beta_peak(self):
        return (self._alpha - 1) / (self._alpha + self._beta - 2)

    @property
    def linear_skew(self):
        _scale_time = self._time / self._end_time
        skew = _scale_time - self.beta_peak
        return skew

    @property
    def quadratic_skew(self):
        _scale_time = self._time / self._end_time
        skew = _scale_time - self.beta_peak
        if skew < 0:
            return -(skew ** 2)
        else:
            return skew ** 2

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, item):
        self._alpha = item

    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, item):
        self._beta = item
