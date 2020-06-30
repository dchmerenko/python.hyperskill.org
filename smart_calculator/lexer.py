# lexer.py

import re

from constants import *
from test_case import test_case_run
import lib


def is_variable(token):
    if not lib.is_valid_name(token):
        raise NameError(f'Invalid identifier: {token}')
    elif token not in var:
        raise NameError(f'Unknown variable: {token}')
    return True


def lexer(input_str):
    '''Gets an expression string and return list of values of numbers, variables and operations.
    2 + 2 -> [2, '+', 2]
    a + b -> [5, '+', 6]
    '''
    previous = None
    expr = input_str.split()
    for i, token in enumerate(expr):
        if lib.is_number(token):
            if previous == VAL:
                raise NameError(f'Invalid expression {token}')
            expr[i] = int(token)
            previous = VAL
        elif lib.is_operator(token):
            if previous == OPR:
                raise NameError(f'Invalid expression {token}')
            expr[i] = lib.get_operator(token)
            previous = OPR
        elif is_variable(token):
            if previous == VAL:
                raise NameError(f'Invalid expression {token}')
            expr[i] = var[token]
            previous = VAL
        else:
            raise NameError(f'Invalid expression {token}')
    return expr


if __name__ == '__main__':

    var = {
        'a': 5,
        'b': 6,
    }

    test_case = {
        '2 + 2': "[2, '+', 2]",
        'a + b': "[5, '+', 6]",
    }

    test_case_run(lexer, test_case)
