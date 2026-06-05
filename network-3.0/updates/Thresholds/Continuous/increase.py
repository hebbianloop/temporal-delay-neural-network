def increase(neuron):
    current_value = neuron.potential + sum(
        (neuron.delay_functions[activation_.input][neuron.time - activation_.time] for
         activation_ in neuron.noncontributing_activations))

    if current_value * (1 - 1 / ((1 / neuron.options['threshold_rate']) + neuron.times_fired)) > neuron.threshold:
        neuron._threshold = current_value * (1 - 1 / ((1 / neuron.options['threshold_rate']) + neuron.times_fired))
