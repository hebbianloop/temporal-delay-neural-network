def contribution(neuron):
    """
    this is a update rule based on the value of the delay functions
    :param neuron: neuron.IntegrateFire
    """
    weight_redistribution = 0
    sum_of_active_inputs = sum(function.value for function in neuron.contributing_functions)
    contributing_inputs = set([function.input for function in neuron.contributing_functions])

    for input_ in neuron.inputs_and_variables:

        #  if an input is not Contributing and its weight would not become less than or equal to 0
        if input_ not in contributing_inputs and \
                                neuron.inputs_and_variables[input_].value - neuron.options['variable_rate'] >= 0:
            # reduce the inputs weight and add it to the redistribution value
            neuron.inputs_and_variables[input_].value -= neuron.options['variable_rate']
            weight_redistribution += neuron.options['variable_rate']

    # distribute the redist value based on the value of each delay function
    for function in neuron.contributing_functions:
        neuron.inputs_and_variables[function.input].value += weight_redistribution * (
            function.value / sum_of_active_inputs)
