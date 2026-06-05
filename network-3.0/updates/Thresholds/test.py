def test(neuron):
    current_value = neuron.potential + sum(
        (neuron.delay_functions[activation_.input][neuron.time - activation_.time] for
         activation_ in neuron.noncontributing_activations))

    if (current_value * (
                1 - ((1 - neuron.options['threshold_rate']) * (1 / (neuron.times_fired + 1))))) * .95 > neuron.threshold:
        neuron._threshold = (current_value * (
            1 - ((1 - neuron.options['threshold_rate']) * (1 / (neuron.times_fired + 1))))) * .95
