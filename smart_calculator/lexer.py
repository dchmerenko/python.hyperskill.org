# lexer.py

import re

from constants import *
import lib


def is_operator(str_):
    return (
        all(c in '+-' for c in str_)
    )


def is_variable(token):
    if not lib.is_valid_name(token):
        raise NameError(f'Invalid identifier: {token}')
    elif token not in var:
        raise NameError(f'Unknown variable: {token}')
    return True


def get_operator(str_):
    if str_.count('+') > 0 or str_.count('-') > 0:
        return SUB if str_.count(SUB) % 2 else ADD


def lexer(input_str):
    '''Gets an expression string and return list of values of numbers, variables and operations.
    >>> lexer('1 +++ 2 -+-- 3')
    [1, '+', 2, '-', 3]
    >>> lexer('a + b')
    [5, '+', 6]
    >>> lexer('c')
    Traceback (most recent call last):
    ...
    NameError: Unknown variable: c
    >>> lexer('c22c')
    Traceback (most recent call last):
    ...
    NameError: Invalid identifier: c22c
    >>> lexer('a = 7 - 8')
    Traceback (most recent call last):
    ...
    NameError: Invalid identifier: =
    '''
    previous = None
    expr = input_str.split()
    for i, token in enumerate(expr):
        if lib.isnumber(token):
            if previous == VAL:
                raise NameError(f'Invalid expression {token}')
            expr[i] = int(token)
            previous = VAL
        elif is_operator(token):
            if previous == OPR:
                raise NameError(f'Invalid expression {token}')
            expr[i] = get_operator(token)
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

    import doctest
    doctest.testmod()
