def equal(neuron):
    """
    This will take the variable rate from all non contributing composite functions and pass it out to the contributing
    composite functions, maintaining the alpha/beta ratio
    :param neuron:
    """

    weight_redistribution = 0
    contributing_inputs = set([activation_.neuron for activation_ in neuron.contributing_activations])

    # this section redistributes weight between mixture models

    # for each non Contributing input remove weight from each composite function of the mixture model
    # todo parallel
    for input_ in neuron.delay_functions:

        # for each set of variables in the mixture model
        for composite in neuron.delay_functions[input_]:
            # if possible remove weight from alpha and add to redistribute
            if composite.alpha - (composite.alpha * neuron.options['variable_rate']) > 0:
                weight_redistribution += composite.alpha * neuron.options['variable_rate']
                composite.alpha -= composite.alpha * neuron.options['variable_rate']

            # if possible remove weight from beta and add to redistribute
            if composite.beta - (composite.beta * neuron.options['variable_rate']) > 0:
                weight_redistribution += composite.beta * neuron.options['variable_rate']
                composite.beta -= composite.beta * neuron.options['variable_rate']

    # each active composite function gets the weight redistribution by the number of active functions
    weight_redistribution /= float(len(neuron.contributing_activations))

    # todo parallel
    for input_ in contributing_inputs:
        # find the list of functions that correspond to that input
        activations = [activation_ for activation_ in neuron.contributing_activations if activation_.input is input_]
        no_of_dists = len(neuron.delay_functions[input_])
        no_activations = len(activations)

        # Add new composite function if required
        if no_activations > no_of_dists:
            neuron.delay_functions[input_].add_functions(no_activations - no_of_dists)

        # order the composite functions by total contribution
        ordered_composites = neuron.delay_functions[input_].ordered_composites(
            [neuron.time - activation_.time for activation_ in activations])

        # pass out the weight redistribution to the composite functions that contributed the most giving the correct
        # ratio to both alpha and beta
        for composite in ordered_composites[:len(activations)]:
            alpha_ratio = composite.alpha / (composite.alpha + composite.beta)
            beta_ratio = composite.beta / (composite.alpha + composite.beta)
            composite.alpha += weight_redistribution * alpha_ratio
            composite.beta += weight_redistribution * beta_ratio

        # this section adjusts the skew of each composite function in the mixture model
        ordered_composites = list(reversed(ordered_composites))
        for _ in activations:
            skewable_composite = ordered_composites.pop()

            # if fire before peak take from alpha and give to beta
            if skewable_composite.linear_skew < 0:
                redist = skewable_composite.alpha * neuron.options['variable_rate'] * -skewable_composite.linear_skew
                if skewable_composite.alpha - redist > 0:
                    skewable_composite.alpha -= redist
                    skewable_composite.beta += redist

                    # otherwise take from beta and give to alpha
            else:
                redist = skewable_composite.beta * neuron.options['variable_rate'] * skewable_composite.linear_skew
                if skewable_composite.beta - redist > 0:
                    skewable_composite.beta -= redist
                    skewable_composite.alpha += redist

    # todo parallel
    for input_ in neuron.delay_functions:
        neuron.delay_functions[input_].recalculate_values()