from collections import deque

from test_case import test_case_run

d = deque()

operator = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2,}

def prec(op):
    return operator[op]

def postfix(expr):
    res = []
    for c in expr:
        if c in ' \t':
            continue
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
    return ''.join(res)


if __name__ == '__main__':

    test_case = {
        'a + b*c + d': 'abc*+d+',
        'a*b*c*d': 'ab*c*d*',
        'a+b*c^d': 'abcd^*+',
        'a+b*c-d*e': 'abc*+de*-',
        '(a+b)*c': 'ab+c*',
        'x^y/(5*z)+10': 'xy^5z*/10+',
        ' 1+ 2 * 3': '123*+',
    }

    test_case_run(postfix, test_case)