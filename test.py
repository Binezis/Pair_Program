import unittest
from argparse import Namespace
from unittest import mock

from Myapp import *


class MyTestCase(unittest.TestCase):

    @mock.patch("Myapp.add_parm")
    def test_main_n_r(self, mock_args):
        mock_args.return_value = Namespace(answer_file=None, exercise_file=None, range=100, sum=100)
        main()
        exercise_file = open("Exercise.txt", "r", encoding='utf-8')
        exercise_lines = exercise_file.readlines()
        answer_file = open("Answer.txt", "r", encoding='utf-8')
        answer_lines = answer_file.readlines()
        exercise_file.close()
        answer_file.close()
        self.assertEqual(len(exercise_lines), 100)
        self.assertEqual(len(answer_lines), 100)

    @mock.patch("Myapp.add_parm")
    def test_main_e_a(self, mock_args):
        mock_args.return_value = Namespace(answer_file="Answer.txt", exercise_file="Exercise.txt", range=None, sum=None)
        main()
        grade_file = open("Grade.txt", "r", encoding='utf-8')
        grade_lines = grade_file.readlines()
        grade_file.close()
        self.assertEqual(grade_lines[1], "Wrong:0 ()")

    @mock.patch("Myapp.add_parm")
    def test_main_none(self, mock_args):
        mock_args.return_value = Namespace(answer_file=None, exercise_file=None, range=None, sum=None)
        self.assertEqual(main(), ValueError)

    def test_add_parm(self):
        self.assertEqual(add_parm(), Namespace(answer_file=None, exercise_file=None, range=None, sum=None))

    def test_out_grade(self):
        grade = out_grade("Exercise.txt", "Answer.txt")
        grade_split = grade.split('\n')
        self.assertEqual(grade_split[1], "Wrong:0 ()")
        grade = out_grade("Exercise.txt", "Wrong.txt")
        grade_split = grade.split('\n')
        self.assertEqual(grade_split[0], "Correct:0 ()")

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

    def test_bracket_answer(self):
        self.assertEqual(bracket_answer("", "", None), None)

    def test_get_proper_fraction(self):
        operator = Operation()
        proper_fraction = operator.get_proper_fraction()
        fraction_split = proper_fraction.split('/')
        self.assertLess(fraction_split[0], fraction_split[1])

    @mock.patch("Myapp.add_parm")
    def test_10000_n(self, mock_args):
        mock_args.return_value = Namespace(answer_file=None, exercise_file=None, range=5, sum=10000)
        main()
        exercise_file = open("Exercise.txt", "r", encoding='utf-8')
        exercise_lines = exercise_file.readlines()
        answer_file = open("Answer.txt", "r", encoding='utf-8')
        answer_lines = answer_file.readlines()
        exercise_file.close()
        answer_file.close()
        self.assertEqual(len(exercise_lines), 10000)
        self.assertEqual(len(answer_lines), 10000)


if __name__ == '__main__':
    unittest.main()
