"""
This is the integrate and fire neuron class.
"""

from neurons import activation
from .super import Neuron


class IntegrateFire(Neuron):
    """
    Integrate and Fire neuron

    methods
        update_delay_functions
            this updates the times for the delay function values and updates the output values if the
            sum of the delay function values are greater than a threshold.
        update_inputs
            this adds new delay functions to the list if the input value changes (called every 10ms for
            the first layer and 1ms for the rest)
        update_variables
            this is called if the threshold value is reached. it updates the weights of all the input
            neurons that have a corresponding delay function at the time it is called
        update_threshold
            this is called to update the threshold based on certain dynamic functions.
        inhibit
            this is called when another neuron fires and the network is inhibitory
    """

    def __init__(self, network, location, inputs, options):
        """
        :rtype: object
        :param network:
        :param location:
        :type inputs: list(_Neuron)
        :param options:
        :return:
        """
        super().__init__(network, location, options)
        self._delay_functions = {input_: self.options.delay_function(input_, options) for input_ in inputs}
        self._threshold = self._options['threshold_start']
        # self._LTD = False  # used for STDP NOT AVAILABLE IN 3.0
        self._contributing_activations = []
        self._noncontributing_activations = []
        self._potential = 0
        self._time_range = 0
        self._times_fired = 0

    def update_inputs(self):

        assert isinstance(self, IntegrateFire)

        # Add new input to Contributing activations
        for input_ in self._delay_functions:
            if input_.value:
                self._contributing_activations.append(activation.Activation(input_, self._network.time))

    def update_delay_functions(self):

        assert isinstance(self, IntegrateFire)

        # Turn neuron off if it is on
        if self._value:
            self._value = False

            # Test for LTD mode. While in LTD mode inputs do not contribute to activation
            # if self._LTD:
            #   Updates.Variables.Weights.ltd(self)

        # Not in LTD mode
        # else:

        # Update Contributing function values
        self._contributing_activations = [activation_ for activation_ in self._contributing_activations if
                                          self.time - activation_.time < self.options['max_delay']]
        # Update noncontributing function values
        self._noncontributing_activations = [activation_ for activation_ in self._contributing_activations if
                                             self.time - activation_.time < self.options['max_delay']]

        # Update neuron potential
        self._potential = sum((self._delay_functions[activation_.input][self.time - activation_.time] for activation_ in
                               self._contributing_activations))

        # Update threshold if using a continuous threshold function
        # if self._options['threshold_function'] in [1, 2, 3, 8]:
        self._update_threshold()

        # Test if neuron fires
        if self._potential >= self._threshold:

            # Neuron fires
            self._value = True

            self._times_fired += 1

            # Update weights
            self._update_delays()

            # Add Contributing activations to noncontributing contributing
            self._noncontributing_activations += self._contributing_activations

            # Find firing time range
            if self._contributing_activations:
                self._time_range = (
                    min((activation_.time for activation_ in self._contributing_activations)),
                    max((activation_.time for activation_ in self._contributing_activations)))

            # Default threshold update location
            # if self._options['threshold_function'] not in [1, 2, 3, 8]:
            #     self._update_threshold()

            # Clear Contributing activations
            self._contributing_activations = []

            # Inhibit all other neurons in layer
            for neuron_ in self._network[self._location[0]]:
                if neuron_ is not self:
                    neuron_.inhibit()

    def inhibit(self):
        """
        This is the inhibition function. can be added to to create different selections/method of inhibition. currently
        when one neuron fires it changes the Contributing functions of all the other neurons to non Contributing
        functions.
        """
        # todo add a LTD style inhibit function, adding a negative exponent to the Contributing functions
        assert isinstance(self, IntegrateFire)
        self._noncontributing_activations += self._contributing_activations
        self._contributing_activations = []

    def _update_delays(self):
        """
        Updates the variables with the function defined in options.
        :return: None
        """
        assert isinstance(self, IntegrateFire)
        self._options.delays_update(self)

    def _update_threshold(self):
        """
        Updates the threshold with the function defined in options.
        :return: None
        """
        assert isinstance(self, IntegrateFire)
        self._options.threshold_update(self)

    # @property NOT AVAILABLE IN 3.0
    # def weight_matrix(self):
    #     assert isinstance(self, IntegrateFire)
    #     out = 'neuron: ' + str(self._location) + '\n' + 'layer, neuron, weight\n'
    #     for x in self._inputs_and_variables:
    #         out += str(x.location[0]) + ', ' + str(x.location[1]) + ', ' + str(self._inputs_and_variables[x]) + '\n'
    #     return out

    # @property
    # def beta_matrix(self):
    #     assert isinstance(self, IntegrateFire)
    #     out = 'neuron: ' + str(self._location) + '\n' + 'layer, neuron, alpha, beta\n'
    #     for x in sorted(self._inputs_and_variables.keys()):
    #         out += str(x.location[0]) + ', ' + str(x.location[1]) + ', ' + str(self._inputs_and_variables[x]) + '\n'
    #     return out
    #
    @property
    def mixture_matrix(self):
        assert isinstance(self, IntegrateFire)
        out = 'neuron: ' + str(self._location) + '\n' + 'layer, neuron, alpha 1, beta 1, alpha 2, beta 2, ...\n'
        for x in sorted(self.delay_functions.keys()):
            out += str(x.location[0]) + ', ' + str(x.location[1]) + ', ' + str(self.delay_functions[x]) + '\n'
        return out

    @property
    def potential(self):
        assert isinstance(self, IntegrateFire)
        return self._potential

    @property
    def threshold(self):
        assert isinstance(self, IntegrateFire)
        return self._threshold

    @property
    def times_fired(self):
        assert isinstance(self, IntegrateFire)
        return self._times_fired

    @property
    def delay_functions(self):
        assert isinstance(self, IntegrateFire)
        return self._delay_functions

    @property
    def noncontributing_activations(self):
        assert isinstance(self, IntegrateFire)
        return self._noncontributing_activations

    @property
    def time(self):
        """
        The current time of the network.
        :return: int
        """
        assert isinstance(self, IntegrateFire)
        return self._network.time

    def __str__(self):
        assert isinstance(self, IntegrateFire)
        data = {'firing time': self._network.time,
                'location': self._location,
                'neuron potential': self._potential,
                'neuron threshold': self._threshold,
                'time range': self._time_range}
        return str(data) + '\n'
