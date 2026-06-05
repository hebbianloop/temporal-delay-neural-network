from DataStructures import data
import Neurons

__author__ = 'James'
"""
the base network:
methods:
    run(file)
        This is the main learning method.
    time
        The time of the network.
    options
        Returns the network options object
"""


# todo make Network a super class with subclasses FeedForward and Random
class FeedForward:
    """
    HELP GOES HERE
    """

    def __init__(self, options_, prefix):
        """
        :type options_: options.Options
        """
        self._options = options_
        self._time = 0
        self._network = []
        self._input = None
        self._log = open(prefix + '_firing_log.txt', 'w')  # The firing log
        self._potentials = None
        if self._options['potential_log']:  # The log for neuron potentials
            self._potentials = open(prefix + '_potential_log.txt', 'w')
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
                    self._network[0].append(Neurons.Input(self, (0, x), self._options))  # network, location, options
            else:  # All other neurons
                for x in range(layer):
                    self._network[i].append(Neurons.IntegrateFire(self, (i, x), self._network[i - 1],
                                                                  self._options))  # network, location, inputs, options

    def run(self, file,prefix):

        self._log = open(prefix + '_firing_log.txt', 'a')  # The firing log
        self._log.write('new iteration\n')
        if self._options['potential_log']:  # The log for neuron potentials
            self._potentials = open(prefix + '_potential_log.txt', 'a')
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
                    assert isinstance(neuron_, Neurons.IntegrateFire)
                    noncontributing_potential = sum(function.value for function in neuron_.noncontributing_functions)
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

        :type item: tuple
        """
        if isinstance(item, tuple):
            i, j = item
            return self._network[i][j]
        else:
            return self._network[item]
