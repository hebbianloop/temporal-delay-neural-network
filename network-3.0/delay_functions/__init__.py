from .beta import Beta
from .beta_mixture import BetaMix


def delay_function(item):
    delay_functions = {1: None,
                       2: Beta,
                       3: BetaMix
                       }
    return delay_functions[item]
