"""
This is the beta mixture delay function
"""

from .super import DelayFunction
from .beta import Beta


class BetaMix(DelayFunction):
    def __init__(self, input_, options):
        super().__init__(input_, options)
        self._mixture = []
        for i in range(options['number_of_distributions']):
            self._mixture.append(Beta(self._input, self._options))
        self._values = [sum(x) / len(self._mixture) for x in zip(*[beta._values for beta in self._mixture])]

    def ordered_composites(self, times):
        """
        Returns a list of the composites ordered by their contribution at times. the greatest is first.
        """
        return list(reversed(sorted(self._mixture[:], key=lambda: self._mixture[:][times])))

    def add_functions(self, number):
        for i in range(number):
            self._mixture.append(Beta(self._input, self._options))

    def __len__(self):
        return len(self._mixture)

    def __getitem__(self, item):
        return self._mixture[item]

    def recalculate_values(self):
        # todo parallel
        for beta in self._mixture:
            beta.recalculate_values()
        self._values = [sum(x) / len(self._mixture) for x in zip(*[beta._values for beta in self._mixture])]

    def __str__(self):

        a = ', '.join([str(self._mixture[beta]) for beta in self._mixture])
        return a