def equal(neuron):
    """
    this is an even weight redistribution. each active input gets an equal proportion of the sum of the weights
    of the inactive inputs.
    :param neuron: neuron.IntegrateFire
    """
    weight_redistribution = 0
    number_of_active_inputs = len(neuron.contributing_functions)
    contributing_inputs = set([function.input for function in neuron.contributing_functions])

    for input_ in neuron.inputs_and_variables:  # this double loop eats time

        #  if an input is not Contributing and its weight would not become less than or equal to 0
        if input_ not in contributing_inputs and \
                                neuron.inputs_and_variables[input_].value - neuron.options['variable_rate'] >= 0:
            # reduce the input's weight and add it to the redistribution value
            neuron.inputs_and_variables[input_].value -= neuron.options['variable_rate']
            weight_redistribution += neuron.options['variable_rate']

    # distribute the redist value equally across the Contributing functions
    for function in neuron.contributing_functions:
        neuron.inputs_and_variables[function.input].value += weight_redistribution / number_of_active_inputs
