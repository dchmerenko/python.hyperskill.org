# operation
CALC = 'calculation'
EMPTY = ''
EXIT = '/exit'
HELP = '/help'
INVALID_EXP = 'Invalid expression'
WRONG_CMD = 'Unknown process_command'

NUMBER = 'number'
OPERATOR = 'operator'

ADD = '+'
SUB = '-'
ASSIGN = '='

# variable
var = {}

def main():
    # process_statement loop
    while True:
        action, expression = process_input()
        if action == EMPTY:
            continue
        elif action == WRONG_CMD:
            print(WRONG_CMD)
        elif action == INVALID_EXP:
            print(INVALID_EXP)
        elif action == HELP:
            show_help()
        elif action == EXIT:
            do_exit()
            break
        elif action == CALC:
            do_calculation(expression)
        else:
            print("Unexpected behevior")


def process_input():
    input_str = input()
    print(input_str, end='\t')  # debug mode
    expression = input_str.split()
    if not expression:
        return EMPTY, None
    elif expression[0].startswith('/'):
        return get_action(expression[0]), None
    else:
        return get_expression(expression)


def get_action(command):
    if command in (HELP, EXIT):
        return command
    return WRONG_CMD


def show_help():
    print('The program calculates the sum or sub of numbers.\n'
          'Type /help for this Help\n'
          '     /exit for terminate program\n'
          'Example:\n'
          '> -2 + 5 - -1\n'
          '4')


def do_exit():
    print('Bye!')


def get_expression(expression):
    # print(expression)
    previous = None
    for i, token in enumerate(expression):
        if is_number(token):
            if previous == NUMBER:
                return INVALID_EXP, None
            expression[i] = int(token)
            previous = NUMBER
        elif is_operator(token):
            if previous == OPERATOR:
                return INVALID_EXP, None
            expression[i] = get_operation(token)
            previous = OPERATOR
        elif is_variable(token):
            if previous == OPERATOR:
                return INVALID_EXP, None
            expression[i] = var[token]
            previous = NUMBER
        else:
            return INVALID_EXP, None
    return CALC, expression


def is_number(str_):
    try:
        int(str_)
        return True
    except ValueError:
        return False


def is_operator(str_):
    return (
        all(c in '+-' for c in str_)
        or '=' in str_
    )


def is_variable(token):
    raise NotImplementedError


def get_operation(str_):
    if str_.count('+') > 0 or str_.count('-') > 0:
        return SUB if str_.count(SUB) % 2 else ADD
    elif str_.count('=') == 1:
        return ASSIGN


def do_calculation(expression):
    result = calculate(expression)
    print(result)


def calculate(expression):
    operation = {
        ADD: lambda a, b: a + b,
        SUB: lambda a, b: a - b,
        }
    # print(expression)
    result = expression[0]
    for operator, number in zip(expression[1::2], expression[2::2]):
        result = operation[operator](result, number)
    return result


def test_main():
    import io
    import sys

    '''
    >>> 2 + 2
    4
    >>> 2 2
    Invalid expression
    >>> /go
    Unknown process_command
    >>> a2a
    Invalid identifier
    >>> n22
    Invalid identifier
    >>> a = 8
    >>> b = c
    Unknown variable
    >>> e
    Unknown variable
    >>> a1 = 8
    Invalid identifier
    >>> n1 = a2a
    Invalid identifier
    >>> n = a2a
    Invalid assignment
    >>> a = 7 = 8
    Invalid assignment   
    >>> /exit
    Bye!
    '''

    input_str = '''2 + 2
2 2
/go
a2a
n22
a = 8
b = c
e
a1 = 8
n1 = a2a
n = a2a
a = 7 = 8
/exit
    '''

    tmp = sys.stdin
    sys.stdin = io.StringIO(input_str)

    main()

    sys.stdin = tmp


if __name__ == '__main__':
    test_main()
