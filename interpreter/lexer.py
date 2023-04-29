

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
        for token in self.full_tokens:
            print(token)

    def read_from_file(self) -> list[str]:
        file = open(self.filename, 'r')
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
                if char == '"' or in_quotes:
                    in_quotes = True
                    if char == '"':
                        q_counter += 1
                    if q_counter % 2 == 0 and temp_str != '"':
                        in_quotes = False
                        temp_str += char
                        self.tokens.append(temp_str)
                        self.full_tokens.append((i, temp_str))
                        temp_str = ""
                    temp_str += char
                elif not char.isalnum():
                    if self.clean_tokens(temp_str) and temp_str != '"':
                        self.tokens.append(temp_str)
                        self.full_tokens.append((i, temp_str))
                        temp_str = ""
                    if self.clean_tokens(char) and char != '"':
                        self.tokens.append(char)
                        self.full_tokens.append((i, char))

                else:
                    temp_str += char
