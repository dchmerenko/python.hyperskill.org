# operation
CALC = 'calculation'
EMPTY = ''
EXIT = '/exit'
HELP = '/help'
INVALID_EXP = 'Invalid expression'
WRONG_CMD = 'Unknown command'

NUMBER = 'number'
OPERATOR = 'operator'

ADD = '+'
SUB = '-'


def main():
    # main loop
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
    expression = input().split()
    if not expression:
        return EMPTY, None
    elif expression[0].startswith('/'):
        return get_action(expression[0]), None
    else:
        return clear(expression)


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


def clear(expression):
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
        else:
            # raise NotImplementedError("Can't handle operation", token)
            return INVALID_EXP, None
    return CALC, expression


def is_number(str_):
    try:
        int(str_)
        return True
    except ValueError:
        return False


def is_operator(str_):
    return all(c in '+-' for c in str_)


def get_operation(str_):
    return SUB if str_.count(SUB) % 2 else ADD


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


if __name__ == '__main__':
    main()
