import io
import sys


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
        raise NameError('Unknown process_command')


def calculate(s):
    print(f'Culculate {s}')


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
    1
    a
    2 + 2
    /go
    /help
    /exit
    '''

    tmp = sys.stdin
    sys.stdin = io.StringIO(input_str)

    process_input()

    sys.stdin = tmp
