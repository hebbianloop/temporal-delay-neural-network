def equal(neuron):
    """
    an equal variable redistribution for the beta functions
    :param neuron: neuron.IntegrateFire
    """
    # redistribute weight from inactive inputs
    weight_redistribution = 0
    number_of_active_inputs = len(neuron.contributing_functions)
    contributing_inputs = set([function.input for function in neuron.contributing_functions])

    for input_ in neuron.inputs_and_variables:
        #  if an input is not Contributing and its weight would not become less than or equal to 1
        if input_ not in contributing_inputs:
            # reduce alpha if possible and add to redist value
            if (neuron.inputs_and_variables[input_].value['alpha'] - 1) * neuron.options['variable_rate'] > 0:
                weight_redistribution += (neuron.inputs_and_variables[input_].value[
                                              'alpha'] - 1) * neuron.options['variable_rate']
                neuron.inputs_and_variables[input_].value['alpha'] -= (neuron.inputs_and_variables[input_].value[
                                                                         'alpha'] - 1) * neuron.options['variable_rate']
            # reduce beta if possible and add to redist value
            if (neuron.inputs_and_variables[input_].value['beta'] - 1) * neuron.options['variable_rate'] > 0:
                weight_redistribution += (neuron.inputs_and_variables[input_].value['beta'] - 1) * neuron.options[
                    'variable_rate']
                neuron.inputs_and_variables[input_].value['beta'] -= (neuron.inputs_and_variables[input_].value[
                                                                        'beta'] - 1) * neuron.options['variable_rate']

    # distribute the redist value equally across the Contributing functions
    for function in neuron.contributing_functions:
        neuron.inputs_and_variables[function.input].value['alpha'] += weight_redistribution / (
            number_of_active_inputs * 2)
        neuron.inputs_and_variables[function.input].value['beta'] += weight_redistribution / (number_of_active_inputs * 2)

    # adjust peak of distribution
    for function in neuron.contributing_functions:
        # if fire before peak take from alpha and give to beta
        if function.quadratic_skew < 0:
            redist = neuron.inputs_and_variables[function.input].value['alpha'] * neuron.options[
                'variable_rate'] * -function.quadratic_skew
            if neuron.inputs_and_variables[function.input].value['alpha'] - redist > 1:
                neuron.inputs_and_variables[function.input].value['alpha'] -= redist
                neuron.inputs_and_variables[function.input].value['beta'] += redist
        # otherwise take from beta and give to alpha
        else:
            redist = neuron.inputs_and_variables[function.input].value['beta'] * neuron.options[
                'variable_rate'] * function.quadratic_skew
            if neuron.inputs_and_variables[function.input].value['beta'] - redist > 1:
                neuron.inputs_and_variables[function.input].value['beta'] -= redist
                neuron.inputs_and_variables[function.input].value['alpha'] += redist
