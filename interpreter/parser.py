from typing import Any
from .utils.errors import *
from .keywords import types, keywords


class Parser:

    def __init__(self, tokens: list[str], full_tokens: list[tuple[int, str]]):
        self.tokens = tokens
        self.full_tokens: list[tuple[int, str]] = full_tokens
        self.variables: dict[str, tuple[Any, str]] = {}
        self.tkns_not_recognised: list[str] = []
        self.parser()
    
        print(self.variables)
    
    def end_code(self):
        print("Variables")
        print(self.variables)
        print("Not Recognised Tokens")
        print(self.tkns_not_recognised)


    def handle_var_declaration(self, i) -> int:
        counter: int = i + 1
        var_name: str = ""
        var_type: str = ""
        flag: bool = False
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

            match var_type:
                case "int":
                    self.variables.update(
                        {var_name: (int(self.tokens[counter]), 'int')})
                case "float":
                    self.variables.update(
                        {var_name: (float(self.tokens[counter]), 'float')})
                case "str":
                    if self.tokens[counter].count('"') != 2:
                        raise StringAssignError
                    self.variables.update(
                        {var_name: (str(self.tokens[counter]).replace('"', ''), 'str')})
                case "bool":
                    self.variables.update(
                        {var_name: (bool(self.tokens[counter]), 'bool')})

        return counter

    def handle_var_assignment(self, i: int) -> int:
        var_name = self.tokens[i]
        counter: int = i + 1

        if self.tokens[counter] == "=":
            counter += 1
        else:
            return counter

        data = self.variables.get(var_name, "")
        var_type: str = data[1]

        match var_type:

            case "int":
                self.variables.update(
                    {var_name: (int(self.tokens[counter]), var_type)})
            case "float":

                self.variables.update(
                    {var_name: (float(self.tokens[counter]), var_type)})

            case "str":

                self.variables.update(
                    {var_name: (str(self.tokens[counter]), var_type)})

            case "bool":

                self.variables.update(
                    {var_name: (bool(self.tokens[counter]), var_type)})

        return counter

    def parser(self) -> None:
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]

            if token == "let":
                i = self.handle_var_declaration(i)
            elif token in self.variables:
                i = self.handle_var_assignment(i)
            elif token == "const":
                pass
            elif token not in keywords:
                self.tkns_not_recognised.append(token)

            i += 1
