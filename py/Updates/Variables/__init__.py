from Updates.Variables import fixed


def updates(delay_function, variable_function):
    if delay_function == 1:
        from Updates.Variables import Weights
        update_functions = {0: fixed,
                            1: Weights.stdp,
                            2: Weights.contribution,
                            3: Weights.contribution_alt1,
                            4: Weights.contribution_alt2,
                            5: Weights.equal,
                            }

    elif delay_function == 2:
        from Updates.Variables import Beta
        update_functions = {0: fixed,
                            1: Beta.linear_equal,
                            2: Beta.linear_contribution,
                            3: Beta.quadratic_equal,
                            4: Beta.quadratic_contribution
                            }

    elif delay_function == 3:
        from Updates.Variables import Mixture
        update_functions = {0: fixed,
                            1: Mixture.contribution_linear_equal,
                            2: Mixture.contribution_quadratic_contribution,
                            3: Mixture.contribution_quadratic_equal,
                            4: Mixture.contribution_quadratic_equal_strong,
                            5: Mixture.equal_linear_equal,
                            6: Mixture.equal_quadratic_equal,
                            7: Mixture.test
                            }
    else:
        update_functions = None

    return update_functions[variable_function]
