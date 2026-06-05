from math import exp


def ltd(neuron):  # todo shady implement
    """
    the ltd part of the Spike Timing Dependent Plasticity rule
    :param neuron:
    :return:
    """
    tauneg = 33.7
    #taupos = 16.8
    apos = 0.03125
    aneg = 0.85 * apos

    neuron._LTD -= neuron._options['network_speed']
    for function in neuron._contributing_functions:
        #print(((tauneg * (neuron.options['max_delay'] / 10.0)) - neuron._LTD) / tauneg)
        neuron._inputs_and_variables[function.input].value -= aneg * exp(-(
                ((tauneg*(neuron.options['max_delay'] / 10.0)) - neuron._LTD) / tauneg))
        if neuron._inputs_and_variables[function.input].value < 0:
            neuron._inputs_and_variables[function.input].value = 0
    neuron._contributing_functions = []
