# operation
EMPTY = ''
HELP = '/help'
EXIT = '/exit'
CALC = '/calc'
ADD = '+'
SUB = '-'


def main():
    # main loop
    while True:
        action, expression = process_input()
        if action == EMPTY:
            continue
        elif action == HELP:
            show_help()
            continue
        elif action == EXIT:
            do_exit()
            break
        else:
            do_calculation(expression)


def process_input():
    expression = input().split()
    if not expression:
        action, expression = EMPTY, None
    elif expression[0] in (HELP, EXIT):
        action, expression = expression[0], None
    else:
        action, expression = CALC, clear(expression)
    return action, expression


def show_help():
    print('The program calculates the sum or sub of numbers.\nExample: > -2 + 5 - -1\n4')


def do_exit():
    print('Bye!')


def clear(expression):
    # print(expression)
    for i, token in enumerate(expression):
        if is_number(token):
            expression[i] = int(token)
        else:
            expression[i] = SUB if token.count(SUB) % 2 else ADD
    return expression


def is_number(str_):
    try:
        int(str_)
        return True
    except ValueError:
        return False


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

