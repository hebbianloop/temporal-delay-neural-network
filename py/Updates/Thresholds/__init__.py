def updates(item):
    from .fixed import fixed
    from .Continuous import maximum as continuous_maximum
    from .Continuous import increase as continuous_increase
    from .Continuous import adaptive_maximum as continuous_adaptive_maximum
    from .Contributing import maximum as contributing_maximum
    from .Contributing import increase as contributing_increase
    from .Contributing import adaptive_maximum as contributing_adaptive_maximum
    from .Contributing import adaptive_increase as contributing_adaptive_increase

    from.test import test

    threshold_update_functions = {0: fixed,
                                  1: continuous_maximum,
                                  2: continuous_increase,  # rubbish
                                  3: continuous_adaptive_maximum,
                                  4: contributing_maximum,
                                  5: contributing_increase,  # rubbish
                                  6: contributing_adaptive_maximum,
                                  7: contributing_adaptive_increase,  # rubbish
                                  8: test}

    return threshold_update_functions[item]
