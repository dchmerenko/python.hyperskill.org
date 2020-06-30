# parser.py

# TODO: Wrong Error handle
# p = Parser('5-3++2')
# 53-Sintax error +
# +2+


class Postfix:
    '''
    Parser converts infix notation to postfix notation (Reverse Polish Notation)
    >>> p = Postfix('9 - 5 + 2')
    >>> p.expr()
    9 5 - 2 +
    '''
    def gen(self):
        for w in self.infix_str.split():
            yield w

    def __init__(self, string):
        self.infix_str = string
        self.g = self.gen()
        self.lookahead = self.read()

    def read(self):
        return next(self.g, None)

    def expr(self):
        self.term()
        while True:
            if self.lookahead == '+':
                self.match('+')
                self.term()
                print('+', end=' ')
            elif self.lookahead == '-':
                    self.match('-')
                    self.term()
                    print('-', end=' ')
            else:
                return

    def term(self):
        if self.lookahead.isdigit():
            print(self.lookahead, end=' ')
            self.match(self.lookahead)
        else:
            print('Sintax error', self.lookahead)

    def match(self, t):
        if self.lookahead == t:
            self.lookahead = self.read()
        else:
            print('Sintax error', self.lookahead)


if __name__ == '__main__':
    p = Postfix('9 - 5 + 2')
    p.expr()  # 9 5 - 2 +
    print()
