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
