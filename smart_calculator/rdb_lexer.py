# Лексический анализ
# разбивает строку на токены
# токен это терминал с дополнительной информацией
# в строке токены представлены лексемами

# Схема трансляции

# expr -> expr + term {print('+')}
#       | expr - term {print('-')}
#       | term

# term -> term * factor {print('*')}
#       | term / factor {print('-')}
#       | factor

# factor -> (expr)
#       | num {print('num.value')}
#       | id  {print('id.lexeme')}

# '22 + 3333 + var'  ->  <Num, 22> <+> <Num, 3333> <+> <Tag.ID, var>

#   rdb_lexer.py

from enum import Enum

from lib import is_number


class Tag(Enum):
    NUM = 256
    ID = 257
    TRUE = 258
    FALSE = 259


class Token:
    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return f'<{self.tag}>'


class Num(Token):
    def __init__(self, v):
        super().__init__(Tag.NUM)
        self.value = int(v)

    def __str__(self):
        return f'<Num, {self.value}>'


class Word(Token):
    def __init__(self, tag, s):
        super().__init__(tag)
        self.lexeme = s

    def __str__(self):
        return f'<{self.tag}, {self.lexeme}>'


class Lexer:
    '''
    '22 + 3333 + var'  # <Num, 22> <+> <Num, 3333> <+> <Tag.ID, var>
    >>> lex = Lexer()
    >>> input_str = '22 + 3333 + var'  # <Num, 22> <+> <Num, 3333> <+> <Tag.ID, var>
    >>> print(' '.join(str(lex.scan(w)) for w in input_str.split()))
    <Num, 22> <+> <Num, 3333> <+> <Tag.ID, var>
    '''
    words = {}

    def reserve(self, t):
        self.words[t.lexeme] = t

    def __init__(self):
        self.reserve(Word(Tag.TRUE, 'true'))
        self.reserve(Word(Tag.FALSE, 'false'))

    def scan(self, token):
        ''' Return token object from token string.'''
        # number processing
        if is_number(token):
            return Num(token)
        # keyword & identifiers processing
        elif token.isalpha():
            w = self.words.get(token)
            if w is not None:
                return w
            w = Word(Tag.ID, token)
            self.words[token] = w
            return w
        # operation token processing (neither number no var)
        return Token(token)


if __name__ == '__main__':
    lex = Lexer()
    input_str = '22 + 3333 + var'  # <Num, 22> <+> <Num, 3333> <+> <Tag.ID, var>
    print(input_str)
    print(' '.join(str(lex.scan(w)) for w in input_str.split()))

    # import doctest
    # doctest.testmod()
