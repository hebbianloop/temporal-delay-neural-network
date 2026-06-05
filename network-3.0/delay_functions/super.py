"""
This contains the superclass for all delay functions.
"""


class DelayFunction:
    def __init__(self, input_, options):
        self._input = input_
        self._options = options
        self._values = []
        self._end_time = self._options['max_delay']

    @property
    def input(self):
        return self._input

    def value(self, times):
        """
        take either a single time or a list of times and returns the sum of values for those times.
        :param times:
        :return:
        """
        if isinstance(times, int):
            return self._values[times]
        else:
            sum(self._values[time] for time in times)
