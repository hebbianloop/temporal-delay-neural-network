"""
This is the beta delay function.
"""

import math
from .super import DelayFunction


class Beta(DelayFunction):
    def __init__(self, input_, options):
        super().__init__(input_, options)
        self._alpha = 2.0
        self._beta = 2.0

        # todo think about parallel
        for i in range(self._end_time):
            _beta_func = math.exp(
                math.lgamma(self._alpha + self._beta) - (math.lgamma(self._alpha) + math.lgamma(self._beta)))
            _scale_time = i / self._end_time
            if _scale_time == 0 or _scale_time == 1:
                self._values.append(0)
            else:
                self._values.append(
                    (((1 - _scale_time) ** (self._beta - 1)) * _scale_time ** (self._alpha - 1)) * _beta_func)

    def recalculate_values(self):
        self._values = []
        # todo think about parallel
        for i in range(self._end_time):
            _beta_func = math.exp(
                math.lgamma(self._alpha + self._beta) - (math.lgamma(self._alpha) + math.lgamma(self._beta)))
            _scale_time = i / self._end_time
            if _scale_time == 0 or _scale_time == 1:
                self._values.append(0)
            else:
                self._values.append(
                    (((1 - _scale_time) ** (self._beta - 1)) * _scale_time ** (self._alpha - 1)) * _beta_func)

    @property
    def beta_peak(self):
        return (self._alpha - 1) / (self._alpha + self._beta - 2)

    def linear_skew(self, time):
        _scale_time = time / self._end_time
        skew = _scale_time - self.beta_peak
        return skew

    def quadratic_skew(self, time):
        _scale_time = time / self._end_time
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

    def __str__(self):
        return str(self.alpha) + ', ' + str(self.beta)
