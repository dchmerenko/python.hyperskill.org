# lib.py

import re


def isnumber(s):
    '''
    Returns True if s is negative or positive whole number else False.
    Example:

    >>> isnumber('5')
    True
    >>> isnumber('-5')
    True
    >>> isnumber('- 5')
    False
    >>> isnumber('0')
    True
    >>> isnumber('a')
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
