import unittest
from fibonacci.fibonacci import (NaiveRecursion,
                                 TailRecursion,
                                 Sequential,
                                 MatricesNumpy,
                                 MatricesManuallyRepeatedMultiplication,
                                 MatricesManuallyRepeatedSquaring,
                                 MatricesEigenValue,
                                 MatricesLargestEigenValue)


class TestFibonacci(unittest.TestCase):
    def setUp(self):
        self.fibonacci_methods = [f() for f in [NaiveRecursion,
                                                TailRecursion,
                                                Sequential,
                                                MatricesNumpy,
                                                MatricesManuallyRepeatedMultiplication,
                                                MatricesManuallyRepeatedSquaring]]
        self.approx_fibonacci_methods = [f() for f in [MatricesEigenValue,
                                                       MatricesLargestEigenValue]]

    def test_invalid_input_throws(self):
        for fibonacci_method in self.fibonacci_methods:
            with self.assertRaises(ValueError, msg=f"The method {type(fibonacci_method).__name__} should throw a value error for negative inputs."):
                fibonacci_method(-1)

    def test_first_few_terms(self):
        fibonacci_numbers = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        for fibonacci_method in self.fibonacci_methods:
            for n, v in enumerate(fibonacci_numbers):
                self.assertEqual(v, fibonacci_method(n), f"The method {type(fibonacci_method).__name__} does not return the correct value {v = } for input {n = }")

    def test_medium_terms(self):
        scalable_fibonacci_methods = [f for f in self.fibonacci_methods if not isinstance(f, NaiveRecursion)]
        for fibonacci_method in scalable_fibonacci_methods:
            # Reference values taken from https://r-knott.surrey.ac.uk/Fibonacci/fibtable.html
            reference_values = {50: 12586269025,
                                51: 20365011074,
                                52: 32951280099,
                                53: 53316291173,
                                54: 86267571272,
                                55: 139583862445, }
            for n, v in reference_values.items():
                self.assertEqual(v, fibonacci_method(n), f"The method {type(fibonacci_method).__name__} does not return the correct value {v = } for input {n = }")

    def test_large_terms(self):
        scalable_fibonacci_methods = [f for f in self.fibonacci_methods if not isinstance(f, (NaiveRecursion, MatricesNumpy))]
        for fibonacci_method in scalable_fibonacci_methods:
            # Reference values taken from https://r-knott.surrey.ac.uk/Fibonacci/fibtable.html
            reference_values = {100: 354224848179261915075,
                                101: 573147844013817084101,
                                102: 927372692193078999176,
                                103: 1500520536206896083277,
                                104: 2427893228399975082453,
                                105: 3928413764606871165730, }
            for n, v in reference_values.items():
                self.assertEqual(v, fibonacci_method(n), f"The method {type(fibonacci_method).__name__} does not return the correct value {v = } for input {n = }")

    def test_massive_terms(self):
        scalable_fibonacci_methods = [f for f in self.fibonacci_methods if isinstance(f, (MatricesManuallyRepeatedMultiplication, Sequential))]
        for fibonacci_method in scalable_fibonacci_methods:
            # Reference values taken from https://mersennus.net/fibonacci/f1000.txt
            reference_values = {995: 5 * 397 * 83629033601 * 436782169201002048261171378550055269633 * 1337873301998533414875239339276051370134922822925229050035977065459942781 * 40403554071088151520608002852733631820943995131673257705056154379655473264829041021,
                                996: 2 ** 4 * 3 ** 2 * 499 * 6464041 * 20276569 * 35761381 * 6202401259 * 93750172283 * 245329617161 * 43084912634851 * 1033043205255409 * 10341247759646081 * 99194853094755497 * 572087591261946589 * 23812215284009787769 * 212216314620580244514251999177476639338737695720283,
                                997: 1993 * 5976017 * 98102710780517 * 25013378664247449571576319242327981 * 351091114524199570730427421619945029084957644098669013217327405859402054908216008832249544669174178909820684413614297716980411650822138944562214697121,
                                998: 997 * 10979 * 492013 * 3074837 * 72376853400026778781 * 242476693680113970844399844268665411909828940569848174382224682362558460739162851 * 57128608773902499888960755640879595424590122515509365520944618528846769695130838292100993,
                                999: 2 * 17 * 53 * 73 * 109 * 149 * 1997 * 2221 * 12653 * 16061684237 * 124134848933957 * 1459000305513721 * 930507731557590226767593761 * 1687733481506255251903139456476245146806742007876216630876557 * 49044806374722940739127188459343134898237532255227554514970877,
                                1000: 3 * 5 ** 3 * 7 * 11 * 41 * 101 * 151 * 251 * 401 * 2161 * 3001 * 4001 * 570601 * 9125201 * 112128001 * 1353439001 * 5738108801 * 28143378001 * 5465167948001 * 10496059430146001 * 84817574770589638001 * 158414167964045700001 * 9372625568572722938847095612481183137496995522804466421273200001, }
            for n, v in reference_values.items():
                self.assertEqual(v, fibonacci_method(n), f"The method {type(fibonacci_method).__name__} does not return the correct value {v = } for input {n = }")

    def test_approx_methods(self):
        reference_method = Sequential()
        for approx_method in self.approx_fibonacci_methods:
            for n in range(15, 20):
                tolerance = 1e-5
                self.assertAlmostEqual(reference_method(n), approx_method(n), delta=tolerance * reference_method(n), msg=f"The answer from our approximate method {type(approx_method).__name__} does not match the reference method {type(reference_method).__name__}")



if __name__ == '__main__':
    unittest.main()
