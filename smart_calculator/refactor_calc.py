import re
import io
import sys

from test_data import *

# constants
ADD = '+'
OPR = 'opr'
SUB = '-'
VAL = 'val'

var = {}


def isnumber(s):
    '''Returns True if s is negative or positive whole number else False.'''
    return s.startswith('-') and s[1:].isdigit() or s.isdigit()


def is_valid_name(name):
    '''Returns True if name consists of Latin symbols only.'''
    return bool(re.match(r'[A-Za-z]+$', name))


def is_assignment(input_str):
    '''Checks that the assignment is in the string.'''
    return input_str.count('=')


def check_lvalue(lvalue):
    '''Checks lvalue name is valid.'''
    if not is_valid_name(lvalue):
        raise NameError(f'Invalid identifier')


def is_operator(str_):
    return all(c in '+-' for c in str_)


def is_variable(token):
    if not is_valid_name(token):
        raise NameError(f'Invalid identifier')
    elif token not in var:
        raise NameError(f'Unknown variable')
    return True


def get_operator(str_):
    if str_.count('+') > 0 or str_.count('-') > 0:
        return SUB if str_.count(SUB) % 2 else ADD


def lexer(input_str):
    previous = None
    expr = input_str.split()
    for i, token in enumerate(expr):
        if isnumber(token):
            if previous == VAL:
                raise NameError(f'Invalid expression')
            expr[i] = int(token)
            previous = VAL
        elif is_operator(token):
            if previous == OPR:
                raise NameError(f'Invalid expression')
            expr[i] = get_operator(token)
            previous = OPR
        elif is_variable(token):
            if previous == VAL:
                raise NameError(f'Invalid expression')
            expr[i] = var[token]
            previous = VAL
        else:
            raise NameError(f'Invalid expression')
    return expr


def evaluate(expr):
    operation = {
        ADD: lambda a, b: a + b,
        SUB: lambda a, b: a - b,
    }
    result = expr[0]
    for operator, number in zip(expr[1::2], expr[2::2]):
        result = operation[operator](result, number)
    return result


def is_empty(s):
    return not s


def is_command(s):
    return s.startswith('/')


def command(s):
    if s == '/help':
        print("Use '+', '-' and 'a = 1', 'abc = a' for whole numbers calculating.",
              "Type '/help' for help, '/exit' for exit.", sep='\n')
    elif s == '/exit':
        print('Bye!')
        sys.exit()
    else:
        raise NameError('Unknown command')


def calculate(s):
    try:
        if is_assignment(s):
            lvalue, rvalue = (expr.strip() for expr in s.split('=', 1))
            check_lvalue(lvalue)
            name = lvalue
            expr = lexer(rvalue)
            var[name] = evaluate(expr)
        else:
            expr = lexer(s)
            msg = f'{evaluate(expr)}'
            print(msg)
    except NameError as exc:
        print(exc)


def process_input():
    while True:
        try:
            input_str = input().strip()
            if is_empty(input_str):
                continue
            elif is_command(input_str):
                command(input_str)
            else:
                calculate(input_str)
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
    process_input()
    #
    # sys.stdin = tmp

