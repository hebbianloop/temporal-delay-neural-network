import delay_functions

__author__ = 'James'


class Options:
    def __init__(self):
        """
        The constructor for the Options object
        :type command_line: list[str]
        """

        self._options = {
            'shape_vector': [20, 1],
            'network_speed': 1,
            'inhibitory': True,
            'max_delay': 17,  # duration of delay function  --> time/20 fed into beta --> should increase by layer
            'delay_function': 3,  # 1 - mesquilier ;; 2 - beta ;; 3 - betamixture
            'threshold_function': 3,  # 1 - fixed ;; 2 - contributing max ;; 3 - contributing & non contributing max
            'threshold_start': 1,
            'threshold_rate': 0.95,  # learning rate, taken from the max of the potential
            'variable_function': 5,  # update rule for alpha and betas
            'variable_rate': .1,
            'potential_log': True,
            'number_of_distributions': 10
        }

    @property
    def delay_function(self):
        return delay_functions.delay_function(self._options["delay_function"])

    def __getitem__(self, item):
        return self._options[item]