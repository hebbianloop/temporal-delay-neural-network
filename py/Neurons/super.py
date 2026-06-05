"""
This is the Neuron superclass.
"""


class Neuron:
    def __init__(self, network, location, options):
        """
        :type location: tuple  # the layer and position of the neuron
        """
        self._value = False
        self._network = network
        self._location = location
        self._options = options

    @property
    def value(self):
        return self._value

    @property
    def location(self):
        return self._location

    def __str__(self):
        return str(self._location) + ', ' + str(self._network.time)

    def __gt__(self, other):
        if self.location[1] > other.location[1]:
            return True
        else:
            return False

    @property
    def options(self):
        return self._options
