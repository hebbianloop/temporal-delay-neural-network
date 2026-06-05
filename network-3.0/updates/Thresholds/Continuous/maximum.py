def maximum(neuron):
    """
    Moves the threshold to be the threshold rate of the max value of the sum of the delay functions (both
    Contributing and noncontributing). This threshold continuously updates, NOT just when the neuron fires.
    :param neuron:
    """

    current_value = neuron.potential + sum(
        (neuron.delay_functions[activation_.input][neuron.time - activation_.time] for
         activation_ in neuron.noncontributing_activations))

    if current_value * neuron.options['threshold_rate'] > neuron.threshold:
        neuron._threshold = current_value * neuron.options['threshold_rate']
