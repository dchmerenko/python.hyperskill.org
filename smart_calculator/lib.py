# lib.py

import re


def is_empty(s):
    '''
    >>> is_empty('')
    True
    >>> is_empty(' ')
    True
    >>> is_empty('\t')
    True
    >>> is_empty('1')
    False
    '''
    return not s.strip()


def is_number(s):
    '''
    Returns True if s is negative or positive whole number else False.
    Example:

    >>> is_number('5')
    True
    >>> is_number('-5')
    True
    >>> is_number('- 5')
    False
    >>> is_number('0')
    True
    >>> is_number('a')
    False
    '''
    return s.startswith('-') and s[1:].isdigit() or s.isdigit()


def is_valid_name(name):
    '''Returns True if name consists of Latin symbols only.
    >>> is_valid_name('a')
    True
    >>> is_valid_name('aaa')
    True
    >>> is_valid_name('a1a')
    False
    >>> is_valid_name('aa1')
    False
    >>> is_valid_name('_')
    False
    >>> is_valid_name('русский')
    False
    '''
    return bool(re.match(r'[A-Za-z]+$', name))


def is_variable(token):
    if not is_valid_name(token):
        raise NameError(f'Invalid identifier: {token}')
    elif token not in var:
        raise NameError(f'Unknown variable: {token}')
    return True


def is_operator(s):
    '''
    >>> is_operator('+++')
    True
    >>> is_operator('+--')
    True
    >>> is_operator('*')
    True
    >>> is_operator('*/^')
    False
    '''
    return all(c in '+-' for c in s) or s in list('*/^')


def get_operator(s):
    '''
    >>> get_operator('+-')
    '-'
    >>> get_operator('--')
    '+'
    >>> get_operator('^')
    '^'
    '''
    if '+' in s or '-' in s:
        return '-' if s.count('-') % 2 else '+'
    return s


def evaluate(b, a, op):
    '''
    >>> evaluate(1, 2, '+')
    3
    >>> evaluate(1, 2, '-')
    -1
    >>> evaluate(1, 2, '*')
    2
    >>> evaluate(1, 2, '/')
    0
    >>> evaluate(1, 2, '^')
    1
    '''
    operation = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a // b,
            '^': lambda a, b: a ** b,
        }
    try:
        return operation[op](a, b)
    except IndexError:
        raise NameError('Invalid expression')



if __name__ == '__main__':
    import doctest
    doctest.testmod()
