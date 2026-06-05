def contribution_alt2(neuron):
    """
    An alternate version of the update rule based on the value of the delay functions. doesn't let weights go to
     0. should be faster.
    :param neuron: IntegrateFire
    """

    weight_redistribution = 0
    sum_of_active_inputs = sum(function.value for function in neuron.contributing_functions)

    # reduce the input weights and add them to the redistribution value
    for input_ in neuron.inputs_and_variables:
        if neuron.inputs_and_variables[input_].value - neuron.options['variable_rate'] >= 0:
            neuron.inputs_and_variables[input_].value -= neuron.options['variable_rate']
            weight_redistribution += neuron.options['variable_rate']

    # distribute the redistribution value based on the value of each delay function
    for function in neuron.contributing_functions:
        neuron.inputs_and_variables[function.input].value += weight_redistribution * (
            function.value / sum_of_active_inputs)
