def increase(neuron):
    max_value = sum(function.value for function in neuron.contributing_functions)
    current_value = max_value + sum(function.value for function in neuron.noncontributing_functions)
    if current_value * (1 - 1 / ((1 / neuron.options['threshold_rate']) + neuron.times_fired)) > neuron.threshold:
        neuron._threshold = current_value * (1 - 1 / ((1 / neuron.options['threshold_rate']) + neuron.times_fired))
