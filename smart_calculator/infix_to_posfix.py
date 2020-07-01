from collections import deque

from test_case import test_case_run


operator = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2,}


def prec(op):
    return operator[op]


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


if __name__ == '__main__':

    test_case = {
        'a + b * c + d': 'a b c * + d +',
        'a * b * c * d': 'a b * c * d *',
        'a + b * c ^ d': 'a b c d ^ * +',
        'a + b * c - d * e': 'a b c * + d e * -',
        '( a + b ) * c': 'a b + c *',
        'x ^ y / ( 5 * z ) + 10': 'x y ^ 5 z * / 10 +',
        ' 1 + 2 * 3': '1 2 3 * +',
        '123 + 25 ^ a': '123 25 a ^ +',
        '-1 + -2': '-1 -2 +',
        '-1 + 2': '-1 2 +',
        '10 * 2 + 2 * 3 + 3 * ( 2 + 3 )': '10 2 * 2 3 * + 3 2 3 + * +',
        '2 - 1': '2 1 -',
    }

    test_case_run(infix_to_postfix, test_case)