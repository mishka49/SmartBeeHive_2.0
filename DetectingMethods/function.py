from datetime import datetime
from scipy.optimize import curve_fit


class FunctionTools:
    @staticmethod
    def approximation(values_x, values_y, function):
        args, _ = curve_fit(function, values_x, values_y)
        print(f"END approximation:")
        return FunctionTools.__approximated_function(*args)(function)

    @staticmethod
    def is_drastic_function_loss(function, value_x, value_y, max_deviation: float) -> bool:
        return function(value_x) - value_y > max_deviation

    @staticmethod
    def is_drastic_function_up(function, value_x, value_y, max_deviation: float) -> bool:
        return value_y - function(value_x) > max_deviation

    @staticmethod
    def __approximated_function(*args):
        def decorator(func):
            func_args = args

            def function(x):
                nonlocal func_args
                return func(x, *func_args)

            return function

        return decorator
