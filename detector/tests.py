from django.test import TestCase


class DetectorTest:
    def test_check_critical_situations(self):
        pass

    def test_create_function(self):
        pass


def test_approximation():
    function = lambda k, b, x: k * x + b

    time = [10, 20, 30, 40]
    weight = [25, 25.2, 25.4, 25.6]

    from DetectingMethods.function import FunctionTools

    aprox_func = FunctionTools.approximation(time, weight, function)

    assert aprox_func(50) == 25.8
