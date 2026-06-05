def maximum(neuron):
    """
    Moves the threshold to be the threshold rate of the max value of the sum of the delay functions (both
    Contributing and noncontributing). This threshold continuously updates, NOT just when the neuron fires.
    :param neuron:
    """

    max_value = sum(function.value for function in neuron.contributing_functions)
    current_value = max_value + sum(function.value for function in neuron.noncontributing_functions)
    if current_value * neuron.options['threshold_rate'] > neuron.threshold:
        neuron._threshold = current_value * neuron.options['threshold_rate']
