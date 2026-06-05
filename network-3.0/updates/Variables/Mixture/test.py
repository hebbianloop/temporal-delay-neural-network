def test(neuron):
    """
    First attempt at a variable update rule for multimodal distribution with fixed number of distributions
    :param neuron:
    :return:
    """
    # todo fix disappearing weight
    weight_redistribution = 0
    sum_of_active_inputs = sum(function.value for function in neuron.contributing_functions)
    contributing_inputs = set([function.input for function in neuron.contributing_functions])

    # this section redistributes weight between mixture models

    # for each non Contributing input remove weight from each composite function of the mixture model
    for input_ in set(neuron.inputs_and_variables) - contributing_inputs:
        no_of_dists = len(neuron.inputs_and_variables[input_])
        # for each set of variables in the mixture model
        for var in (neuron.inputs_and_variables[input_]):
            # if possible remove weight from alpha and add a scaled amount to be redistributed
            if var.value['alpha'] - var.value['alpha'] * neuron.options['variable_rate'] > 0:
                weight_redistribution += (var.value['alpha'] * neuron.options['variable_rate'])
                var.value['alpha'] -= var.value['alpha'] * neuron.options['variable_rate']

            # if possible remove weight from beta and add a scaled amount to be redistributed
            if var.value['beta'] - var.value['beta'] * neuron.options['variable_rate'] > 0:
                weight_redistribution += (var.value['beta'] * neuron.options['variable_rate'])
                var.value['beta'] -= var.value['beta'] * neuron.options['variable_rate']
    #print(weight_redistribution)
    # for each Contributing function assign an equal amount of a weight to each composite function of the corresponding
    # mixture model. The weight is determined by the value of the function.
    # #print(weight_redistribution, 'weight redist')
    for function in neuron.contributing_functions:
        no_of_dists = len(neuron.inputs_and_variables[function.input])
        redist = (weight_redistribution / sum_of_active_inputs) * function.value
        # #print(redist, 'input')
        for var in neuron.inputs_and_variables[function.input]:
            # #print(var.value['alpha'], var.value['beta'], 1)
            var.value['alpha'] += (redist / no_of_dists) / 2
            var.value['beta'] += (redist / no_of_dists) / 2
            # #print(var.value['alpha'], var.value['beta'], 2)

    # this section redistributes weight between the composite functions of each mixture model equally
    # #print(arg1.mixture_matrix)
    for input_ in contributing_inputs:
        # find the list of functions that correspond to that input
        activations = [function for function in neuron.contributing_functions if function.input is input_]
        no_of_dists = len(neuron.inputs_and_variables[input_])
        no_activations = len(activations)

        # add new composite functions if required
        if no_activations > no_of_dists:
            neuron.inputs_and_variables[input_].add_function(no_activations - no_of_dists)
        no_of_dists = len(neuron.inputs_and_variables[input_])

        # find the total contribution of each composite function
        sum_composite_values = activations[0].composite_values
        for function in activations[1:]:
            sum_composite_values = list(map(lambda x, y: x + y, sum_composite_values, function.composite_values))

        # order the composite functions by total contribution
        ordered_composite_indices = (sorted(range(len(sum_composite_values)), key=lambda i: sum_composite_values[i]))

        # #print(ordered_composite_indices, sum_composite_values, no_activations)

        # #print('input', no_activations)
        weight_redist = 0
        # for the least Contributing composites, number of composites - number of activations
        for i in ordered_composite_indices[:no_of_dists - no_activations]:
            # #print('here')

            # remove some weight from alpha and add to the redist
            if neuron.inputs_and_variables[input_][i].value['alpha'] - neuron.inputs_and_variables[input_][i].value[
                'alpha'] * neuron.options['variable_rate'] > 0:
                weight_redist += (neuron.inputs_and_variables[input_][i].value['alpha']) * neuron.options[
                    'variable_rate']
                neuron.inputs_and_variables[input_][i].value['alpha'] -= (neuron.inputs_and_variables[input_][i].value[
                                                                            'alpha']) * neuron.options[
                                                                           'variable_rate']
            # remove some weight from beta and add to redist
            if neuron.inputs_and_variables[input_][i].value['beta'] - neuron.inputs_and_variables[input_][i].value['beta'] * \
                    neuron.options['variable_rate'] > 0:
                weight_redist += (neuron.inputs_and_variables[input_][i].value['beta']) * neuron.options[
                    'variable_rate']
                neuron.inputs_and_variables[input_][i].value['beta'] -= (neuron.inputs_and_variables[input_][i].value[
                                                                           'beta']) * neuron.options['variable_rate']

        # #print(arg1.inputs_and_variables[input_]._mixture)
        # pass out the redist to the composite functions that contributed the most based equally
        for i in ordered_composite_indices[no_of_dists - no_activations:]:
            # #print('here again', weight_redist, i)
            #   #print(arg1.inputs_and_variables[input_][i].value['alpha'], ' alpha ',
            #        arg1.inputs_and_variables[input_][i].value['beta'], ' beta')
            neuron.inputs_and_variables[input_][i].value['alpha'] += ((weight_redist / no_activations) / 2)
            neuron.inputs_and_variables[input_][i].value['beta'] += ((weight_redist / no_activations) / 2)
            #  #print(arg1.inputs_and_variables[input_][i].value['alpha'], ' alpha ',
            #       arg1.inputs_and_variables[input_][i].value['beta'], ' beta')

        # TEST SECTION even out the weights between active distributions
        redist = 0
        for i in ordered_composite_indices[no_of_dists - no_activations:]:
            redist += neuron.inputs_and_variables[input_][i].value['alpha'] * neuron.options['variable_rate']
            redist += neuron.inputs_and_variables[input_][i].value['beta'] * neuron.options['variable_rate']
            neuron.inputs_and_variables[input_][i].value['alpha'] -= neuron.inputs_and_variables[input_][i].value['alpha'] * neuron.options['variable_rate']
            neuron.inputs_and_variables[input_][i].value['beta'] -= neuron.inputs_and_variables[input_][i].value['beta'] * neuron.options['variable_rate']

        for i in ordered_composite_indices[no_of_dists - no_activations:]:
            neuron.inputs_and_variables[input_][i].value['alpha'] += ((redist / no_activations) / 2)
            neuron.inputs_and_variables[input_][i].value['beta'] += ((redist / no_activations) / 2)

        # this section adjusts the skew of each composite function in the mixture model

        available_composite_indices = list(range(len(neuron._inputs_and_variables[input_])))
        # #print((available_composite_indices))
        for function in activations:
            # find the beta composite function that is to be skewed and remove it from the list of available composite
            # functions. this ensures no single composite function has its skew adjusted by multiple activation times.
            skewable_composite_index = None
            x = 0
            while skewable_composite_index is None:
                # #print(x, len(function.composite_values))
                if x <= len(function.composite_values) - 1:
                    if list(reversed(
                            sorted(range(len(sum_composite_values)), key=lambda i: function.composite_values[i])))[
                        x] in available_composite_indices:
                        skewable_composite_index = \
                            list(reversed(
                                sorted(range(len(sum_composite_values)), key=lambda i: function.composite_values[i])))[
                                x]
                        available_composite_indices.remove(skewable_composite_index)
                        skewable_composite = function[skewable_composite_index]
                else:
                    skewable_composite_index = available_composite_indices[0]
                    available_composite_indices.remove(skewable_composite_index)
                    skewable_composite = 'break'
                x += 1
            # #print(skewable_composite_index)
            # todo remove #print statements
            # if fire before peak take from alpha and give to beta
            if skewable_composite != 'break':
                if skewable_composite.linear_skew < 0:
                    redist = neuron.inputs_and_variables[input_][skewable_composite_index].value['alpha'] * neuron.options[
                        'variable_rate'] * -skewable_composite.linear_skew
                    # redist = arg1.inputs_and_variables[input_][skewable_composite_index].value['alpha'] * -skewable_composite.quadratic_skew
                    if neuron.inputs_and_variables[input_][skewable_composite_index].value['alpha'] - redist > 0:
                        neuron.inputs_and_variables[input_][skewable_composite_index].value['alpha'] -= redist
                        neuron.inputs_and_variables[input_][skewable_composite_index].value['beta'] += redist

                # otherwise take from beta and give to alpha
                else:
                    redist = neuron.inputs_and_variables[input_][skewable_composite_index].value['beta'] * neuron.options[
                        'variable_rate'] * skewable_composite.linear_skew
                    # redist = arg1.inputs_and_variables[input_][skewable_composite_index].value['beta'] * skewable_composite.quadratic_skew
                    if neuron.inputs_and_variables[input_][skewable_composite_index].value['beta'] - redist > 0:
                        neuron.inputs_and_variables[input_][skewable_composite_index].value['beta'] -= redist
                        neuron.inputs_and_variables[input_][skewable_composite_index].value['alpha'] += redist

        for function in activations:
            function.update_weights(neuron.inputs_and_variables[input_])
