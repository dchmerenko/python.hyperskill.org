import re
import io
import sys

from test_data import *
import lib
import infix_to_posfix

# constants
OPR = 'operator'
VAL = 'value'

var = {}


def is_assignment(input_str):
    '''Checks that the assignment is in the string.'''
    return input_str.count('=')


def check_lvalue(lvalue):
    '''Checks lvalue name is valid.'''
    if not lib.is_valid_name(lvalue):
        raise NameError(f'Invalid identifier')


def is_variable(token):
    if not lib.is_valid_name(token):
        raise NameError(f'Invalid identifier')
    elif token not in var:
        raise NameError(f'Unknown variable')
    return True


def lexer(input_str):
    '''2 + 2 -> [2, '+', 2]'''
    previous = None
    expr = input_str.split()
    for i, token in enumerate(expr):
        if lib.is_number(token):
            if previous == VAL:
                raise NameError(f'Invalid expression')
            expr[i] = int(token)
            previous = VAL
        elif lib.is_operator(token):
            if previous == OPR:
                raise NameError(f'Invalid expression')
            expr[i] = lib.get_operator(token)
            previous = OPR
        elif is_variable(token):
            if previous == VAL:
                raise NameError(f'Invalid expression')
            expr[i] = var[token]
            previous = VAL
        else:
            raise NameError(f'Invalid expression')
    return expr


def is_empty(s):
    return not s


def is_command(s):
    return s.startswith('/')


def process_command(s):
    if s == '/help':
        print("Use '+', '-' and 'a = 1', 'abc = a' for whole numbers calculating.",
              "Type '/help' for help, '/exit' for exit.", sep='\n')
    elif s == '/exit':
        print('Bye!')
        sys.exit()
    else:
        raise NameError('Unknown process_command')


def process_statement(s):
    try:
        if is_assignment(s):
            lvalue, rvalue = (expr.strip() for expr in s.split('=', 1))
            check_lvalue(lvalue)
            name = lvalue
            expr = lexer(rvalue)
            var[name] = lib.evaluate(expr)
        else:
            expr = lexer(s)
            expr = infix_to_posfix.postfix(expr)
            msg = f'{lib.evaluate(expr)}'
            print(msg)
    except NameError as exc:
        print(exc)


def calculator_run():
    while True:
        try:
            input_str = input().strip()
            if is_empty(input_str):
                continue
            elif is_command(input_str):
                process_command(input_str)
            else:
                process_statement(input_str)
        except NameError as exc:
            print(exc)


if __name__ == '__main__':

    input_str = '''
    a  =  3
    b= 4
    c =5
    a + b - c
    b - c + 4 - a
    a = 800
    a + b + c
    BIG = 9000
    BIG
    big
    /exit
    '''
    # a  =  3
    # b= 4
    # c =5
    # a + b - c  # 2
    # b - c + 4 - a  # 0
    # a = 800
    # a + b + c  # 809
    # BIG = 9000
    # BIG  # 9000
    # big  # Unknown variable
    # /exit  # Bye!

    # tmp = sys.stdin
    # sys.stdin = io.StringIO(input_str)
    #
    calculator_run()
    #
    # sys.stdin = tmp

