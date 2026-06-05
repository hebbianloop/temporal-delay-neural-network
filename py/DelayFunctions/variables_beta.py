"""
This is the beta functions variables object.
"""

from.variables_super import DelayVariables


class AlphaBeta(DelayVariables):
    def __init__(self, options):
        super().__init__(options)
        self._alpha_beta = {'alpha': 2.0, 'beta': 2.0}

    @property
    def value(self):
        """
        Returns alpha and beta as a tuple
        """
        return self._alpha_beta

    def __str__(self):
        return str(self._alpha_beta['alpha']) + ', ' + str(self._alpha_beta['beta'])
