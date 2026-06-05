"""
This is the superclass for delay variables
"""


class DelayVariables:

    def __init__(self, options):
        pass

    @property
    def value(self):
        """
        To be overwritten
        """
        pass

    @value.setter
    def value(self, item):
        """
        To be overwritten
        """
        pass

    def __str__(self):
        """
        To be overwritten
        """
        pass
