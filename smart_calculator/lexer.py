# lexer.py

from collections import deque

import lib


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
            op = lib.get_operator(b)
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



def f(expr):
    try:
        res = lexer(expr)
    except NameError as exc:
        res = repr(exc)
    return res


def test_case_run(f, test_case):

    np = [0, 0]  # [False, True]
    w0 = w1 = w2 = 0

    for test, check in test_case.items():
        t = str(f(test))
        np[t == check] += 1
        w0 = len(str(test)) if w0 < len(str(test)) else w0
        w1 = len(str(t)) if w1 < len(str(t)) else w1
        w2 = len(str(check)) if w2 < len(str(check)) else w2
        print(f'Check: {test:{w0}}'
              f'\tResult: {t:{w1}}'
              f'\tExpected: {check:{w2}}'
              f'\tTest: {"Ok" if t == check else "Fail"}'
        )

    msg = (
        f'\nTesting "{f.__name__}(...)" failed. {np[True]} tests passed, {np[False]} tests failed.',
        f'\nTesting "{f.__name__}(...)" complete. All {np[True]} tests is OK.',
    )[np[False] == 0]

    print(msg)


if __name__ == '__main__':

    var = {'a': 1, 'b': 2, 'c': 3, }

    test_case = {
        'a*2+b*3+c*(2+3)': '1 * 2 + 2 * 3 + 3 * ( 2 + 3 )',
        '8 * 3 + 12 * (4 - 2)': '8 * 3 + 12 * ( 4 - 2 )',
        '2 - 2 + 3': '2 - 2 + 3',
        '4 * (2 + 3': '4 * ( 2 + 3',
        '-10': '-10',
        '-a': '-1',
        '1 +++ 2 * 3 -- 4': '1 + 2 * 3 + 4',
        '?': "NameError('Invalid expression: ?',)",
        '3 *** 5': '3 * * * 5',
        '4+3)': '4 + 3 )',
    }

    test_case_run(f, test_case)
