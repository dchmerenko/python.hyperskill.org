# assignment.py

import lib
import evaluate as ev
import lexer as lx

from constants import *


def is_assignment(input_str):
    '''Checks that the assignment is in the string.'''
    return input_str.count('=')


def check_lvalue(lvalue):
    '''Checks lvalue name is valid.'''
    if not lib.is_valid_name(lvalue):
        raise NameError(f'Invalid identifier: {lvalue}')


test_data = [
    'n = 3',
    'm=4',
    'a  =   5',
    'b = a',
    'v=   7',
    'n =9',
    'count = 10',
    'a = 1',
    'a = 2',
    'a = 3',
    'a',  # 3
    #
    # Incorrect spelling or declaration of variables should also throw an exception with the corresponding message to the user:
    # First, the variable is checked for correctness.
    # If the user inputs an invalid variable name, then the output should be "Invalid identifier".
    'a2a',  # Invalid identifier
    'n22',  # Invalid identifier
    #
    # If a variable is valid but not declared yet, the program should print "Unknown variable".
    'a = 8',
    'b = c',  # Unknown variable
    'e',  # Unknown variable
    #
    # If an identifier or value of a variable is invalid during variable declaration, the program must print a message like the one below.
    'a1 = 8',  # Invalid identifier
    'n1 = a2a',  # Invalid identifier
    'n = a2a',  # Invalid assignment
    'd = 7 = 8',  # Invalid assignment
    #
    # Examples:
    #
    'a  =  3',
    'b= 4',
    'c =5',
    'a + b - c',  # 2
    'b - c + 4 - a',  # 0
    'a = 800',
    'a + b + c',  # 809
    'BIG = 9000',
    'BIG',  # 9000
    'big',  # Unknown variable
    '/exit',  # Bye!
]


for input_str in test_data:
    msg = f"'{input_str}'"

    try:
        if is_assignment(input_str):
            lvalue, rvalue = (expr.strip() for expr in input_str.split('=', 1))
            check_lvalue(lvalue)
            # msg += f" '{lvalue}' '{rvalue}'"
            name = lvalue
            expr = lx.lexer(rvalue)
            var[name] = ev.evaluate(expr)
            # print(msg)
        else:
            expr = lx.lexer(input_str)
            msg += f' {ev.evaluate(expr)}'
            print(msg)
    except NameError as exc:
        print(msg, str(exc))
