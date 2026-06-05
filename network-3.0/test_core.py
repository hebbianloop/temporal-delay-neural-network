"""
This is a test core to see if putting all classes in one file allows for parallelism
"""
import math
from multiprocessing.dummy import Pool as ThreadPool

from DataStructures import data

pool = ThreadPool(4)  # Sets the pool size to 4


class FeedForward:
    """
    HELP GOES HERE
    """

    def __init__(self, options_):
        """
        :type options_: options.Options
        """
        self._options = options_
        self._time = 0
        self._network = []
        self._input = None
        self._log = open('firing_log.txt', 'w')  # The firing log
        self._potentials = None
        if self._options['potential_log']:  # The log for neuron potentials
            self._potentials = open('potential_log.txt', 'w')
        self._log.close()
        self._potentials.close()
        print('initialized')
        self._initialise()

    def _initialise(self):
        """
        Initialise the network according to the shape vector
        """

        for i, layer in enumerate(self._options['shape_vector']):
            self._network.append([])
            if i == 0:  # Input neurons
                for x in range(layer):
                    self._network[0].append(Input(self, (0, x), self._options))  # network, location, options
            else:  # All other neurons
                for x in range(layer):
                    self._network[i].append(IntegrateFire(self, (i, x), self._network[i - 1],
                                                          self._options))  # network, location, inputs, options

    def run(self, file):

        self._log = open('firing_log.txt', 'a')  # The firing log
        self._log.write('new iteration\n')
        if self._options['potential_log']:  # The log for neuron potentials
            self._potentials = open('potential_log.txt', 'a')
            self._potentials.write('new iteration\n')
            self._potentials.write(
                'layer, neuron, time, contributing potential, noncontributing potential, total potential, threshold \n')
        self._time = 0
        self._input = data.Data(file)
        if len(self._input.attributes) != self._options['shape_vector'][0]:
            print('incorrect number of inputs')
        else:
            print('running')
            percent = 0
            for i in range(len(self._input) * self._input.speed):  # todo check if this is correct
                self._update()
                if ((float(i) / self._input.speed) / float(len(self._input))) >= percent:
                    print(str(round(percent * 100)) + '%')
                    percent += 0.05
        print('finished')
        if self._potentials is not None:
            self._potentials.close()
        self._log.close()

    def _update(self):

        # Update network inputs
        if self.time % self._input.speed == 0:
            for i, In in enumerate(self._network[0]):
                In.value = self._input.examples[self._time // self._input.speed][i]
            for neuron_ in self._network[1]:
                neuron_.update_inputs()

        # Update non input neurons
        if self.time % self._options['network_speed'] == 0:

            # Update delay functions for first row of non input neurons
            for neuron_ in self._network[1]:
                neuron_.update_delay_functions()

                # Log of neuron potentials
                if self._options['potential_log']:
                    assert isinstance(neuron_, IntegrateFire)
                    noncontributing_potential = sum(
                        (neuron_.delay_functions[activation_.input][self.time - activation_.time] for activation_ in
                         neuron_.noncontributing_activations))
                    self._potentials.write(str(neuron_.location[0]) + ', ' +
                                           str(neuron_.location[1]) + ', ' +
                                           str(self.time) + ', ' +
                                           str(neuron_.potential) + ', ' +
                                           str(noncontributing_potential) + ', ' +
                                           str(neuron_.potential + noncontributing_potential) + ', ' +
                                           str(neuron_.threshold) +
                                           '\n')

                # Firing log
                if neuron_.value:
                    self._log.write(str(neuron_))

            # Update all other neurons
            for i in range(2, len(self._options['shape_vector'])):
                for neuron_ in self._network[i]:
                    neuron_.update_delay_functions()
                    neuron_.update_inputs()

        # Increment network time
        self._time += 1

    @property
    def time(self):
        return self._time

    @property
    def options(self):
        return self._options

    def __getitem__(self, item):

        """

        :type item: tuple|int
        """
        if isinstance(item, tuple):
            i, j = item
            return self._network[i][j]
        else:
            return self._network[item]


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
                self._contributing_activations.append(Activation(input_, self._network.time))

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
        equal(self)

    def _update_threshold(self):
        """
        Updates the threshold with the function defined in options.
        :return: None
        """
        assert isinstance(self, IntegrateFire)
        adaptive_maximum(self)

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
    def contributing_activations(self):
        assert isinstance(self, IntegrateFire)
        return self._contributing_activations

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


class Activation:
    def __init__(self, neuron, time):
        self._neuron = neuron
        self._time = time

    @property
    def neuron(self):
        return self._neuron

    @property
    def time(self):
        return self._time


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


class Beta(DelayFunction):
    def __init__(self, input_, options):
        super().__init__(input_, options)
        self._alpha = 2.0
        self._beta = 2.0

        # todo think about parallel
        for i in range(self._end_time):
            _beta_func = math.exp(
                math.lgamma(self._alpha + self._beta) - (math.lgamma(self._alpha) + math.lgamma(self._beta)))
            _scale_time = i / self._end_time
            if _scale_time == 0 or _scale_time == 1:
                self._values.append(0)
            else:
                self._values.append(
                    (((1 - _scale_time) ** (self._beta - 1)) * _scale_time ** (self._alpha - 1)) * _beta_func)

    def recalculate_values(self):
        self._values = []
        # todo think about parallel
        for i in range(self._end_time):
            _beta_func = math.exp(
                math.lgamma(self._alpha + self._beta) - (math.lgamma(self._alpha) + math.lgamma(self._beta)))
            _scale_time = i / self._end_time
            if _scale_time == 0 or _scale_time == 1:
                self._values.append(0)
            else:
                self._values.append(
                    (((1 - _scale_time) ** (self._beta - 1)) * _scale_time ** (self._alpha - 1)) * _beta_func)

    @property
    def beta_peak(self):
        return (self._alpha - 1) / (self._alpha + self._beta - 2)

    def linear_skew(self, time):
        _scale_time = time / self._end_time
        skew = _scale_time - self.beta_peak
        return skew

    def quadratic_skew(self, time):
        _scale_time = time / self._end_time
        skew = _scale_time - self.beta_peak
        if skew < 0:
            return -(skew ** 2)
        else:
            return skew ** 2

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, item):
        self._alpha = item

    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, item):
        self._beta = item

    def __str__(self):
        return str(self.alpha) + ', ' + str(self.beta)


class BetaMix(DelayFunction):
    def __init__(self, input_, options):
        super().__init__(input_, options)
        self._mixture = []
        for i in range(options['number_of_distributions']):
            self._mixture.append(Beta(self._input, self._options))
        self._values = [sum(x) / len(self._mixture) for x in zip(*[beta._values for beta in self._mixture])]

    def ordered_composites(self, times):
        """
        Returns a list of the composites ordered by their contribution at times. the greatest is first.
        """
        return list(reversed(sorted(self._mixture[:], key=lambda: self._mixture[:][times])))

    def add_functions(self, number):
        for i in range(number):
            self._mixture.append(Beta(self._input, self._options))

    def __len__(self):
        return len(self._mixture)

    def __getitem__(self, item):
        return self._mixture[item]

    def recalculate_values(self):
        # todo probablt wont work
        pool.map(lambda beta: beta.recalculate_values(), self._mixture)
        # for beta in self._mixture:
        #     beta.recalculate_values()
        self._values = [sum(x) / len(self._mixture) for x in zip(*[beta._values for beta in self._mixture])]

    def __str__(self):

        a = ', '.join([str(self._mixture[beta]) for beta in self._mixture])
        return a


def adaptive_maximum(neuron):
    """
    Moves the threshold to be the threshold rate of the max value of the sum of the delay functions (both
    Contributing and noncontributing). This threshold continuously updates, but is always reset to .95 of the
    contributing potential when a neuron fires.
    :param neuron:
    """

    current_value = neuron.potential + sum(
        (neuron.delay_functions[activation_.input][neuron.time - activation_.time] for
         activation_ in neuron.noncontributing_activations))
    if current_value * neuron.options['threshold_rate'] > neuron.threshold:
        neuron._threshold = current_value * neuron.options['threshold_rate']
    if neuron.potential >= neuron.threshold:
        neuron._threshold = neuron.potential * neuron.options['threshold_rate']


def equal(neuron):
    """
    This will take the variable rate from all non contributing composite functions and pass it out to the contributing
    composite functions, maintaining the alpha/beta ratio
    :param neuron:
    """

    weight_redistribution = 0
    contributing_inputs = set([activation_.neuron for activation_ in neuron.contributing_activations])

    # this section redistributes weight between mixture models

    # for each non Contributing input remove weight from each composite function of the mixture model
    # todo parallel
    # for input_ in neuron.delay_functions:
    def take(input_):
        taken_weight = 0
        # for each set of variables in the mixture model
        for composite in neuron.delay_functions[input_]:
            # if possible remove weight from alpha and add to redistribute
            if composite.alpha - (composite.alpha * neuron.options['variable_rate']) > 0:
                taken_weight += composite.alpha * neuron.options['variable_rate']
                composite.alpha -= composite.alpha * neuron.options['variable_rate']

            # if possible remove weight from beta and add to redistribute
            if composite.beta - (composite.beta * neuron.options['variable_rate']) > 0:
                taken_weight += composite.beta * neuron.options['variable_rate']
                composite.beta -= composite.beta * neuron.options['variable_rate']

        return taken_weight

    # each active composite function gets the weight redistribution by the number of active functions
    weight_redistribution = sum(pool.map(take, neuron.delay_functions)) / float(len(neuron.contributing_activations))

    # weight_redistribution /= float(len(neuron.contributing_activations))

    # todo parallel
    # for input_ in contributing_inputs:
    def add_and_skew(input_):
        # find the list of functions that correspond to that input
        activations = [activation_ for activation_ in neuron.contributing_activations if activation_.input is input_]
        no_of_dists = len(neuron.delay_functions[input_])
        no_activations = len(activations)

        # Add new composite function if required
        if no_activations > no_of_dists:
            neuron.delay_functions[input_].add_functions(no_activations - no_of_dists)

        # order the composite functions by total contribution
        ordered_composites = neuron.delay_functions[input_].ordered_composites(
            [neuron.time - activation_.time for activation_ in activations])

        # pass out the weight redistribution to the composite functions that contributed the most giving the correct
        # ratio to both alpha and beta
        for composite in ordered_composites[:len(activations)]:
            alpha_ratio = composite.alpha / (composite.alpha + composite.beta)
            beta_ratio = composite.beta / (composite.alpha + composite.beta)
            composite.alpha += weight_redistribution * alpha_ratio
            composite.beta += weight_redistribution * beta_ratio

        # this section adjusts the skew of each composite function in the mixture model
        ordered_composites = list(reversed(ordered_composites))
        for _ in activations:
            skewable_composite = ordered_composites.pop()

            # if fire before peak take from alpha and give to beta
            if skewable_composite.linear_skew < 0:
                redist = skewable_composite.alpha * neuron.options['variable_rate'] * -skewable_composite.linear_skew
                if skewable_composite.alpha - redist > 0:
                    skewable_composite.alpha -= redist
                    skewable_composite.beta += redist

                    # otherwise take from beta and give to alpha
            else:
                redist = skewable_composite.beta * neuron.options['variable_rate'] * skewable_composite.linear_skew
                if skewable_composite.beta - redist > 0:
                    skewable_composite.beta -= redist
                    skewable_composite.alpha += redist

    pool.map(add_and_skew, contributing_inputs)

    # todo parallel
    pool.map(lambda input_: neuron.delay_functions[input_].recalculate_values(), neuron.delay_functions)
    # for input_ in neuron.delay_functions:
    #     neuron.delay_functions[input_].recalculate_values()
