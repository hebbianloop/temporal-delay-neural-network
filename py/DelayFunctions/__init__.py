def delay_function(item):
    from .function_beta import Beta
    from .function_masq import Masq
    from .function_beta_mixture import BetaMix

    delay_functions = {1: Masq,
                       2: Beta,
                       3: BetaMix
                       }
    return delay_functions[item]


def delay_variable(item):
    from .variables_weight import Weight
    from .variables_beta import AlphaBeta
    from .variables_mixture import Mixture

    delay_variables = {1: Weight,
                       2: AlphaBeta,
                       3: Mixture
                       }
    return delay_variables[item]
