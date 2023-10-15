import pseudo
import os


def test_calculator():
    # call the function to be tested
    pseudo.generate_code("tmp/calculator.txt")


def test_strip_markdown():
    # call the function to be tested
    pseudo.generate_code("tmp/strip_markdown.txt")


def test_func_reader():
    pseudo.get_AST("tmp/func_reader.py")
