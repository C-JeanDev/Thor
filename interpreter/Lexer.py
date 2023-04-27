from enum import Enum, auto


class TokenType(Enum):
    STRING = auto()
    KEYWORD = auto()
    NUMBER = auto()


class Lexer:

    def __init__(self, filename: str):
        self.filename = filename
        self.data = self.read_from_file()
        self.loc: list[str] = []
        self.full_tokens: list[tuple[int, str]] = []
        self.tokens: list[str] = []
        self.lexer()
        self.print_tokens()

    def print_tokens(self) -> None:
        for token in self.tokens:
            print(token)

    def read_from_file(self) -> list[str]:
        file = open(self.filename, 'r')
        print(type(file))
        return [line for line in file if line != '\n']

    def clean_tokens(self, token: str) -> bool:
        if token != ' ' and token != '\t' and token:
            return True
        return False

    def lexer(self) -> None:
        lines: list = self.data

        for i, line in enumerate(lines):

            line = lines[i] = line.replace('\n', ' ')
            temp_str: str = ''
            q_counter: int = 0
            in_quotes: bool = False
            chars = list(line)

            for char in chars:
                if not char.isalnum():
                    if self.clean_tokens(temp_str):
                        self.tokens.append(temp_str)
                        self.full_tokens.append((i, temp_str))
                        temp_str = ""
                    if self.clean_tokens(char):
                        self.tokens.append(char)
                        self.full_tokens.append((i, char))

                elif char == "'" or in_quotes:
                    in_quotes = True
                    if char == "'":
                        q_counter += 1
                    if q_counter % 2 == 0:
                        in_quotes = False
                        self.tokens.append(temp_str)
                        self.full_tokens.append((i, temp_str))
                        temp_str = ""
                    else:
                        temp_str += char
                else:
                    temp_str += char
