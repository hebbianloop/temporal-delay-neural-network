"""
This is the beta mixture delay function
"""

from .function_super import DelayFunction
from .function_beta import Beta


class BetaMix(DelayFunction):
    def __init__(self, input_, options, variables):
        super().__init__(input_, options)
        self._mixture = []
        for var in variables:
            self._mixture.append(Beta(input_, options, var))

    def update_value(self):
        self._time += self._options['network_speed']
        self._value = 0
        for beta in self._mixture:
            beta.update_value()
            self._value += beta.value
        self._value / len(self)
        return self

    def update_weights(self, item):
        for i in range(len(self._mixture)):
            self._mixture[i].update_weights(item[i])

    @property
    def most_contributing_index(self):
        biggest_value = 0
        most_contributing_index = None
        for i, beta in enumerate(self):
            if beta.value > biggest_value:
                biggest_value = beta.value
                most_contributing_index = i
        return most_contributing_index

    @property
    def composite_values(self):
        return [beta.value for beta in self._mixture]

    def __iter__(self):
        for function in self._mixture:
            yield function

    def __len__(self):
        return len(self._mixture)

    def __getitem__(self, item):
        return self._mixture[item]
