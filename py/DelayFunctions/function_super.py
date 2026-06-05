"""
This contains the superclass for all delay functions.
"""


class DelayFunction:
    def __init__(self, input_, options):
        self._input = input_
        self._options = options
        self._time = 0
        self._value = 0
        self._end_time = self._options['max_delay']

    @property
    def input(self):
        return self._input

    @property
    def value(self):
        return self._value

    @property
    def time(self):
        return self._time

    @property
    def finished(self):
        if self._time + self._options['network_speed'] <= self._end_time:
            return False
        else:
            return True

    def update_value(self):
        """
        To be overwritten
        """
        pass
