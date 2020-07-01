import re
import io
import sys
from collections import deque


operator = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2, }

operation = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b,
    '^': lambda a, b: a ** b,
}

var = {}


def is_empty(s):
    return not s


def is_command(s):
    return s.startswith('/')


def process_command(s):
    if s == '/help':
        print("Use '+', '-', '*', '/', '^' and 'a = 1', 'abc = a' for whole numbers calculating.",
              "Real numbers are not allowed."
              "Type '/help' for help, '/exit' for exit.", sep='\n')
    elif s == '/exit':
        print('Bye!')
        sys.exit()
    else:
        raise NameError('Unknown process_command')


def process_statement(s):
    try:
        if is_assignment(s):
            lvalue, rvalue = (val.strip() for val in s.split('=', 1))
            name = process_lvalue(lvalue)
            expr = lexer(rvalue)
            var[name] = calculate(expr)
        else:
            expr = lexer(s)
            print(calculate(expr))
    except NameError as exc:
        print(exc)


def is_assignment(s):
    return '=' in s


def lexer(expr):
    d = deque()
    i = 0
    while i < len(expr):
        if expr[i] in ' \t':
            i += 1
            continue
        elif expr[i] in '*/^()':
            d.append(expr[i])
            i += 1
            continue
        elif expr[i] in '+-':
            b = ''
            while i < len(expr) and expr[i] in '+-':
                b += expr[i]
                i += 1
            op = get_operator(b)
            d.append(op)
            continue
        elif expr[i].isdigit():
            b = ''
            while i < len(expr) and expr[i].isdigit():
                b += expr[i]
                i += 1
            if (len(d) > 2 and not isinstance(d[-2], int) or len(d) == 1) and d[-1] == '-':
                d.pop()
                number = -int(b)
            else:
                number = int(b)
            d.append(number)
            continue
        elif expr[i].isalpha():
            b = ''
            while i < len(expr) and expr[i].isalpha():
                b += expr[i]
                i += 1
            if b not in var:
                raise NameError('Unknown variable')
            if (len(d) > 2 and not isinstance(d[-2], int) or len(d) == 1) and d[-1] == '-':
                d.pop()
                number = -var[b]
            else:
                number = var[b]
            d.append(number)
        else:
            raise NameError(f'Invalid expression: {expr[i]}')

    return ' '.join(str(_) for _ in d)


def get_operator(s):
    if '+' in s or '-' in s:
        return '-' if s.count('-') % 2 else '+'
    return s


def calculate(expr):
    if bracket_check(expr):
        expr = infix_to_postfix(expr)
    else:
        raise NameError('Invalid expression')
    s = deque()
    for c in expr.split():
        if is_number(c):
            s.append(int(c))
        elif is_operator(c):
            try:
                s.append(evaluate(s.pop(), s.pop(), c))
            except IndexError:
                raise NameError('Invalid expression')
    return s.pop()


def is_operator(s):
    return all(c in '+-' for c in s) or s in operator


def evaluate(b, a, op):
    return operation[op](a, b)


def bracket_check(expr):
    bracket = deque()
    for c in expr.split():
        if c == '(':
            bracket.append(c)
        elif c == ')':
            if len(bracket) > 0:
                bracket.pop()
            else:
                return False
    return len(bracket) == 0


def infix_to_postfix(expr):
    d = deque()
    res = []
    for c in expr.split():
        # if c in ' \t':
        #     continue
        if c in operator:
            while d and d[-1] != '(' and prec(c) <= prec(d[-1]):
                res.append(d.pop())
            d.append(c)
        elif c == '(':
            d.append(c)
        elif c == ')':
            while d and d[-1] != '(':
                res.append(d.pop())
            d.pop()
        else:
            res.append(c)
    while d:
        res.append(d.pop())
    return ' '.join(res)


def prec(op):
    return operator[op]


def is_number(s):
    return s.startswith('-') and s[1:].isdigit() or s.isdigit()


def is_valid_name(name):
    return bool(re.match(r'[A-Za-z]+$', name))


def process_lvalue(lvalue):
    if is_valid_name(lvalue):
        return lvalue
    raise NameError(f'Invalid identifier')


def is_variable(token):
    if not is_valid_name(token):
        raise NameError(f'Invalid identifier')
    elif token not in var:
        raise NameError(f'Unknown variable')
    return True


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
    
    2 * 2 *********** 2
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

    tmp = sys.stdin
    sys.stdin = io.StringIO(input_str)

    calculator_run()

    sys.stdin = tmp

