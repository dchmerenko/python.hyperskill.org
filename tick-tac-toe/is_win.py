def is_win(field, mark):
    '''
    >>> is_win('X_X_O____', 'X')
    False
    >>> is_win('XXX_O____', 'X')
    True
    >>> is_win('XOX_O__O_', 'O')
    True
    >>> is_win('X_X_X___X', 'X')
    True
    >>> is_win('X_X_X___X', 'O')
    False
    '''

    # field rows, columns, diagonal names
    r1 = '012'
    r2 = '345'
    r3 = '678'
    c1 = '036'
    c2 = '147'
    c3 = '258'
    md = '048'  # main diagonal
    ad = '246'  # antidiagonal

    return any([
        all([field[int(i)] == mark for i in r1]),
        all([field[int(i)] == mark for i in r2]),
        all([field[int(i)] == mark for i in r3]),
        all([field[int(i)] == mark for i in c1]),
        all([field[int(i)] == mark for i in c2]),
        all([field[int(i)] == mark for i in c3]),
        all([field[int(i)] == mark for i in md]),
        all([field[int(i)] == mark for i in ad]),
    ])

if __name__ == "__main__":
    import doctest
    doctest.testmod()