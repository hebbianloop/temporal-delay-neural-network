"""
This is the weight variable object
"""

from .variables_super import DelayVariables


class Weight(DelayVariables):
    def __init__(self, options):
        super().__init__(options)
        self._weight = 1.0

    @property
    def value(self):
        """
        Returns the weight
        :return: float
        """
        return self._weight

    @value.setter
    def value(self, item):
        """
        Sets the weight
        :param item: float
        :return: None
        """
        self._weight = item

    def __str__(self):
        return str(self._weight)
