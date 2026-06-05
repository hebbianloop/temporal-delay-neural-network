def equal(neuron):
    """
    This will take the variable rate from all non contributing composite functions and pass it out to the contributing
    composite functions, maintaining the alpha/beta ratio
    :param neuron:
    """

    weight_redistribution = 0
    contributing_inputs = set([function.input for function in neuron.contributing_functions])

    # this section redistributes weight between mixture models

    # for each non Contributing input remove weight from each composite function of the mixture model
    for input_ in set(neuron.inputs_and_variables):

        # for each set of variables in the mixture model
        for var in (neuron.inputs_and_variables[input_]):
            # if possible remove weight from alpha and add to redistribute
            if var.value['alpha'] - (var.value['alpha'] * neuron.options['variable_rate']) > 0:
                weight_redistribution += (var.value['alpha'] * neuron.options['variable_rate'])
                var.value['alpha'] -= (var.value['alpha'] * neuron.options['variable_rate'])

            # if possible remove weight from beta and add to redistribute
            if var.value['beta'] - (var.value['beta'] * neuron.options['variable_rate']) > 0:
                weight_redistribution += (var.value['beta'] * neuron.options['variable_rate'])
                var.value['beta'] -= (var.value['beta'] * neuron.options['variable_rate'])

    total_weight = 0
    for input_ in set(neuron.inputs_and_variables):

        # for each set of variables in the mixture model
        for var in (neuron.inputs_and_variables[input_]):
            total_weight += var.value['alpha']
            total_weight += var.value['beta']

    # each active composite function gets the weight redistribution by the number of active functions
    weight_redistribution /= float(len(neuron.contributing_functions))

    for input_ in contributing_inputs:
        # find the list of functions that correspond to that input
        activations = [function for function in neuron.contributing_functions if function.input is input_]
        no_of_dists = len(neuron.inputs_and_variables[input_])
        no_activations = len(activations)

        # Add new composite function if required
        if no_activations > no_of_dists:
            neuron.inputs_and_variables[input_].add_function(no_activations - no_of_dists)
        no_of_dists = len(neuron.inputs_and_variables[input_])

        # find the total contribution of each composite function
        sum_composite_values = activations[0].composite_values
        # #print(sum_composite_values, '1')
        for function in activations[1:]:
            sum_composite_values = list(map(lambda x, y: x + y, sum_composite_values, function.composite_values))

        # order the composite functions by total contribution
        ordered_composite_indices = (sorted(range(len(sum_composite_values)), key=lambda i: sum_composite_values[i]))

        # pass out the weight redistribution to the composite functions that contributed the most giving the correct
        # ratio to both alpha and beta
        for i in ordered_composite_indices[no_of_dists - no_activations:]:
            alpha_ratio = neuron.inputs_and_variables[input_][i].value['alpha'] / \
                          (neuron.inputs_and_variables[input_][i].value['alpha'] +
                           neuron.inputs_and_variables[input_][i].value['beta'])
            beta_ratio = neuron.inputs_and_variables[input_][i].value['beta'] / \
                         (neuron.inputs_and_variables[input_][i].value['alpha'] +
                          neuron.inputs_and_variables[input_][i].value['beta'])
            neuron.inputs_and_variables[input_][i].value['alpha'] += weight_redistribution * alpha_ratio
            neuron.inputs_and_variables[input_][i].value['beta'] += weight_redistribution * beta_ratio

        # this section adjusts the skew of each composite function in the mixture model

        available_composite_indices = list(range(len(sum_composite_values)))

        for function in activations:
            # find the beta composite function that is to be skewed and remove it from the list of available composite
            # functions. this ensures no single composite function has its skew adjusted by multiple activation times.
            skewable_composite_index = None
            x = 0
            if len(available_composite_indices) != 0:
                while skewable_composite_index is None:
                    if list(reversed(
                            sorted(range(len(sum_composite_values)), key=lambda i: function.composite_values[i])))[
                        x] in available_composite_indices:
                        skewable_composite_index = \
                            list(reversed(
                                sorted(range(len(sum_composite_values)), key=lambda i: function.composite_values[i])))[
                                x]
                        available_composite_indices.remove(skewable_composite_index)
                        skewable_composite = function[skewable_composite_index]
                    x += 1
            else:
                skewable_composite = 'break'

            if skewable_composite != 'break':

                # if fire before peak take from alpha and give to beta
                if skewable_composite.quadratic_skew < 0:
                    redist = neuron.inputs_and_variables[input_][skewable_composite_index].value['alpha'] * \
                             neuron.options['variable_rate'] * -skewable_composite.quadratic_skew

                    if neuron.inputs_and_variables[input_][skewable_composite_index].value['alpha'] - redist > 0:
                        neuron.inputs_and_variables[input_][skewable_composite_index].value['alpha'] -= redist
                        neuron.inputs_and_variables[input_][skewable_composite_index].value['beta'] += redist

                # otherwise take from beta and give to alpha
                else:
                    redist = neuron.inputs_and_variables[input_][skewable_composite_index].value['beta'] * \
                             neuron.options['variable_rate'] * skewable_composite.quadratic_skew

                    if neuron.inputs_and_variables[input_][skewable_composite_index].value['beta'] - redist > 0:
                        neuron.inputs_and_variables[input_][skewable_composite_index].value['beta'] -= redist
                        neuron.inputs_and_variables[input_][skewable_composite_index].value['alpha'] += redist
