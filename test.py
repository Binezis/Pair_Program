import unittest
from argparse import Namespace
from unittest import mock

from Myapp import *


class MyTestCase(unittest.TestCase):

    @mock.patch("Myapp.add_parm")
    def test_main_n_r(self, mock_args):
        mock_args.return_value = Namespace(answer_file=None, exercise_file=None, range=100, sum=100)
        self.assertEqual(main(), None)

    @mock.patch("Myapp.add_parm")
    def test_main_e_a(self, mock_args):
        mock_args.return_value = Namespace(answer_file="Answer.txt", exercise_file="Exercise.txt", range=None, sum=None)
        self.assertEqual(main(), None)

    @mock.patch("Myapp.add_parm")
    def test_main_none(self, mock_args):
        mock_args.return_value = Namespace(answer_file=None, exercise_file=None, range=None, sum=None)
        self.assertEqual(main(), None)

    def test_add_parm(self):
        self.assertEqual(add_parm(), Namespace(answer_file=None, exercise_file=None, range=None, sum=None))

    def test_out_grade(self):
        grade = out_grade("Exercise.txt", "Answer.txt")
        grade_split = grade.split('\n')
        print(grade_split[1])
        self.assertEqual(grade_split[1], "Wrong:0 ()")

    def test_check(self):
        b = check(['2', 'x', "1'1/2"], '3', ["1'1/2x2"], ['3'])
        self.assertEqual(b, False)

    def test_is_same(self):
        b = is_same("(4/5+3/5)x1/2", ["1/2x(3/5+4/5)"])
        self.assertEqual(b, True)

    def test_to_fraction(self):
        fraction = to_fraction("89/55")
        self.assertEqual(fraction, "1'34/55")
        fraction = to_fraction("10/5")
        self.assertEqual(fraction, "2")
        fraction = to_fraction("5'10")
        self.assertEqual(fraction, ValueError)


if __name__ == '__main__':
    unittest.main()
