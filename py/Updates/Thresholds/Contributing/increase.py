def increase(neuron):
    max_value = sum(function.value for function in neuron.contributing_functions)
    while len(neuron.contributing_functions) > 0:
        neuron._contributing_functions = [function.update_value() for function in neuron.contributing_functions if
                                          not function.finished]
        if sum(function.value for function in neuron.contributing_functions) > max_value:
            max_value = sum(function.value for function in neuron.contributing_functions)
    if max_value * (1 - (1 / neuron.times_fired)) > neuron.threshold:
        neuron._threshold = max_value * (1 - (1 / neuron.times_fired))