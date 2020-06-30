# evaluate.py

from constants import *


def evaluate(expr):
    '''
    >>> evaluate([-5, '+', 6, '-', 2])
    -1
    >>> evaluate([1])
    1
    '''
    operation = {
        ADD: lambda a, b: a + b,
        SUB: lambda a, b: a - b,
    }
    # print(expression)
    result = expr[0]
    for operator, number in zip(expr[1::2], expr[2::2]):
        result = operation[operator](result, number)
    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod()
