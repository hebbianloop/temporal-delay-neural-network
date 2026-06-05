def maximum(neuron):
    """
    Moves the threshold to be the threshold rate of the max value of the sum of the delay functions that
    contribute to the neurons firing if it exceeds the current threshold
    :param neuron:
    """
    max_value = sum(function.value for function in neuron.contributing_functions)
    while len(neuron.contributing_functions) > 0:
        neuron._contributing_functions = [function.update_value() for function in neuron.contributing_functions if
                                          not function.finished]
        if sum(function.value for function in neuron.contributing_functions) > max_value:
            max_value = sum(function.value for function in neuron.contributing_functions)
    if max_value * neuron.options['threshold_rate'] > neuron.threshold:
        neuron._threshold = max_value * neuron.options['threshold_rate']
