from ..utils.errors import *
import sys
sys.path.append('.')
types = [
    "int", "float", "str", "bool"
]
keywords = [
    "let"
]


class Parser:

    def __init__(self, tokens: list[str], full_tokens: list[tuple[int, str]]):
        self.tokens = tokens
        self.full_tokens: list[tuple[int, str]] = full_tokens
        self.variables: dict = {}
        self.parser()
        print(self.variables)

    def handle_var_declaration(self, i) -> None:
        counter: int = i + 1
        var_name: str = ""
        var_type: str = ""
        flag: bool = False
        print(self.tokens[counter])
        if self.tokens[counter] not in keywords and self.tokens[counter].isalnum():
            var_name = self.tokens[counter]
            counter += 1
        if self.tokens[counter] == ":":
            flag = True
            counter += 1
        if self.tokens[counter] in types:
            var_type = self.tokens[counter]
            counter += 1
        if self.tokens[counter] == "=":
            flag = True
            counter += 1
        if self.tokens[counter] and flag:

            print(var_name, var_type, self.tokens[counter])
            match var_type:
                case "int":
                    self.variables.update(
                        {var_name: int(self.tokens[counter])})
                case "float":
                    self.variables.update(
                        {var_name: float(self.tokens[counter])})
                case "str":
                    if self.tokens[counter].count("'") != 2:
                        raise
                    self.variables.update(
                        {var_name: str(self.tokens[counter])})
                case "bool":
                    self.variables.update(
                        {var_name: bool(self.tokens[counter])})

        counter += 1

    def parser(self) -> None:
        quote_counter: int = 0
        round_b_counter: int = 0
        braces_counter: int = 0

        for i, token in enumerate(self.tokens):

            if token == "let":
                print(token, i)
                self.handle_var_declaration(i)
