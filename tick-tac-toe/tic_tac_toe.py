# Analyze user input and show messages in the following situations:
# - "This cell is occupied! Choose another one!" - if the cell is not empty;
# - "You should enter numbers!" - if the user enters other symbols;
# - "Coordinates should be from 1 to 3!" - if the user goes beyond the field.
# Then output the table including the user's most recent move.


def print_field():
    print('---------')
    print('| {} {} {} |'.format(*field[:4]))
    print('| {} {} {} |'.format(*field[3:7]))
    print('| {} {} {} |'.format(*field[6:]))
    print('---------')


def get_coordinates():
    while True:
        try:
            r, c = input("Enter the coordinates: ").split()
            r, c = int(r), int(c)
        except ValueError:
            print("You should enter numbers!")
            continue
        if not (1 <= r <= 3 and 1 <= c <= 3):
            print("Coordinates should be from 1 to 3!")
            continue
        if field[(3 - r) * 3 + c - 1] in (x, o):
            print("This cell is occupied! Choose another one!")
            continue
        return r, c

def update_field(r, c, mark):
    global field
    field_lst =  list(field)
    field_lst[(3 - r) * 3 + c - 1] = mark
    field = ''.join(field_lst)


def is_win(mark):
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


def get_result():
    x_win = is_win(x)
    o_win = is_win(o)
    diff_qty = field.count(x) - field.count(o)
    wrong_qty = not (-1 <= diff_qty <= 1)
    both_wins = (x_win and o_win)
    if wrong_qty or both_wins:
        return "Impossible"
    if x_win:
        return "X wins"
    if o_win:
        return "O wins"
    if field.count(x) + field.count(o) == len(field):
        return "Draw"
    if any([mark not in (x, o) for mark in field]):
        return "Game not finished"


def main():
    # Enter cells: > X_X_O____
    # ---------
    # | X   X |
    # |   O   |
    # |       |
    # ---------
    # Enter the coordinates: > 1 1
    # ---------
    # | X   X |
    # |   O   |
    # | X     |
    # ---------

    global field

    # Get the 3x3 field from the input.
    field = input("Enter cells: ")

    # Output this 3x3 field with cells before the user's move.
    print_field()

    # Ask the user about his next move.
    r, c = get_coordinates()

    update_field(r, c, mark)

    # Output this 3x3 field with cells after the user's move.
    print_field()

# field marks
x = 'X'
o = 'O'

# user mark
mark = x

# field rows, columns, diagonal names
r1 = '012'
r2 = '345'
r3 = '678'
c1 = '036'
c2 = '147'
c3 = '258'
md = '048'  # main diagonal
ad = '246'  # antidiagonal

if __name__ == '__main__':
    main()
