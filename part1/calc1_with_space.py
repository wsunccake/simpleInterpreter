from enum import Enum
from operator import le


class TokenType(Enum):
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    EOF = 'EOF'


class Token:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f'Token({self.type}, {self.value})'

    def __repr__(self) -> str:
        return self.__str__


class Interpreter:
    """
    >>> Interpreter('1+2').expr()
    3

    >>> Interpreter('1 +2').expr()
    3

    >>> Interpreter('1+ 2').expr()
    3

    >>> Interpreter('1 + 2').expr()
    3

    >>> Interpreter('1 + 2 ').expr()
    3

    >>> Interpreter('1+23').expr()
    24

    >>> Interpreter('1 + 23 ').expr()
    24
    """

    def __init__(self, text) -> None:
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Error pasring input')

    def get_next_token(self):
        text = self.text

        while self.pos < len(text) and text[self.pos] == ' ':
            self.pos += 1

        if self.pos > len(text) - 1:
            token = Token(TokenType.EOF, None)
            return token

        current_char = text[self.pos]

        if current_char.isdigit():
            num_begin = self.pos
            while self.pos < len(text) and text[self.pos].isdigit():
                self.pos += 1
            num_end = self.pos
            token = Token(TokenType.INTEGER, int(text[num_begin:num_end]))
            return token

        if current_char == '+':
            token = Token(TokenType.PLUS, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(TokenType.INTEGER)

        op = self.current_token
        self.eat(TokenType.PLUS)

        right = self.current_token
        self.eat(TokenType.INTEGER)

        result = left.value + right.value
        return result


def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    main()
