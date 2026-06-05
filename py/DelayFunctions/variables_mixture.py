"""
This is the variables object for the beta mixture function.
"""

from .variables_super import DelayVariables
from .variables_beta import AlphaBeta


class Mixture(DelayVariables):
    def __init__(self, options):
        super().__init__(options)
        self._mixture = {}
        self._options = options
        for i in range(options['number_of_distributions']):
            self._mixture[i] = AlphaBeta(options)

    def add_function(self, number):
        """
        Adds n new AlphaBeta objects to the mixture
        :param number: int
        """
        start_index = len(self._mixture)
        for i in range(number):
            self._mixture[start_index + i] = AlphaBeta(self._options)

    @property
    def value(self):
        """
        Returns a list of the values of its component models
        :return: list
        """
        return [variable.value for variable in self]

    @value.setter
    def value(self, item):
        """
        Sets the values for each of its component models
        :param item: list(tuple)
        :return: None
        """
        for i in range(len(self)):
            self[i] = item[i]

    def __iter__(self):
        for alpha_beta in self._mixture:
            yield self._mixture[alpha_beta]

    def __len__(self):
        return len(self._mixture)

    def __setitem__(self, key, item):
        self._mixture[key] = item

    def __getitem__(self, item):
        return self._mixture[item]

    def __str__(self):

        a = ', '.join([str(self._mixture[beta]) for beta in self._mixture])
        return a
