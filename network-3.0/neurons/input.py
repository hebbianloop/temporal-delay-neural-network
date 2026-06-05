"""
This is the input neuron class
"""

from.super import Neuron


class Input(Neuron):
    """
an input neuron only has a single value that is updated based on the data file
"""

    def __init__(self, network, location, options):
        """

        :rtype: object
        """
        super().__init__(network, location, options)

    @Neuron.value.setter
    def value(self, item):
        """
        :type item: bool
        """
        self._value = item
