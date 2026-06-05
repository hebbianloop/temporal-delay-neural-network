from math import exp


def stdp(neuron):  # todo shady implement
    """
    this is the LTP part of Spike Timing Dependent Plasticity rule
    :param neuron:
    """
    # Constants for STDP
    # * * tau+ = 16.8 * maxdelay/10
    # * * tau- = 33.7 * maxdelay/10
    # Lengths for LTP/LTD
    # If any contriutiong functions active during this time period,
    # then change their weights.
    #  LTP: [ ti-tau+, ti ] ... LTD : [ti, ti+tau-]
    tauneg=33.7
    taupos=16.8
    apos=0.03125
    neuron._last_fire=neuron._network.time
    # functoin.time is how long delay function has been on (relative to activation)
    for function in neuron._contributing_functions:
        neuron._inputs_and_variables[function.input].value += apos * exp(-function.time/taupos)
        if neuron._inputs_and_variables[function.input].value > 1:
            neuron._inputs_and_variables[function.input].value = 1

    neuron._LTD = int(tauneg * (neuron.options['max_delay']/10.0))
