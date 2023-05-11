from typing import Any
from dataclasses import dataclass
from .errors import *
from .keywords import types, keywords


@dataclass
class Variable:

    name: str
    data: Any
    var_type: str
    const: bool = False


class Parser:

    def __init__(self, tokens: list[str], full_tokens: list[tuple[int, str]]):
        self.tokens = tokens
        self.full_tokens: list[tuple[int, str]] = full_tokens
        self.variables: dict[str, Variable] = {}
        self.tkns_not_recognised: list[str] = []
        self.parser()
        self.end_code()
    

    def end_code(self):
        print("VARIABLES")
        # print({key:value for (key,value)  in self.variables.items()})
        for key, value in self.variables.items():
            print(f"{key}:{value}\n")
        print("NOT RECOGNISED TOKEN")
        print(self.tkns_not_recognised)

    def handle_declaration(self, i: int, is_const: bool) -> int:
        line: int = i
        counter: int = i + 1
        var_name: str = ""
        var_type: str = ""
        flag: bool = False
        if self.tokens[counter] not in keywords and self.tokens[counter].replace(
                '_', '').isalnum():
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
            is_variable: bool = False
            data: Any = self.tokens[counter]
            if self.tokens[counter] in self.variables:
                is_variable = True
                var: Variable = self.variables.get(
                    self.tokens[counter], Variable("", "", ""))
                var_type = var.var_type
                data = var.data

            op = str(data)

            try:
                while self.full_tokens[counter][0] == self.full_tokens[counter + 1][0]:
                    counter += 1
                    string: str = self.tokens[counter]
                    if self.tokens[counter] not in self.variables and self.tokens[counter].count(
                            '"') == 3:
                        string = self.tokens[counter][1:]
                    elif self.tokens[counter].replace('"', '') in self.variables and self.tokens[counter].count('"') != 2:
                        string = self.variables.get(
                            self.tokens[counter].replace(
                                '"', ''), Variable(
                                "", "", "")).data
                    op += str(string)

            except IndexError as e:
                print(e)

            if '+' in list(op) or var_type != 'str':
                data = eval(op)

            match var_type:
                case "int":
                    self.variables.update({var_name: Variable(
                        var_name, int(data), "int", is_const)})
                case "float":
                    data = str(data)
                    try:
                        while self.full_tokens[counter][0] == self.full_tokens[counter + 1][0]:
                            counter += 1
                            data += self.tokens[counter]
                    except IndexError as e:
                        pass
                    data = float(data)

                    self.variables.update({var_name: Variable(
                        var_name, float(data), "float", is_const)})

                case "str":
                    self.variables.update({var_name: Variable(
                        var_name, data, "str", is_const)})
                case "bool":
                    self.variables.update({var_name: Variable(
                        var_name, bool(data), "bool", is_const)})

        return counter

    def handle_var_assignment(self, i: int) -> int:

        var_name = self.tokens[i]
        counter: int = i + 1

        if self.tokens[counter] == "=":
            counter += 1
        else:
            return counter

        var: Variable = self.variables.get(var_name, Variable("", "", ""))
        if var.const:
            raise

        data: Any = self.tokens[counter]

        if data in self.variables:
            var2: Variable = self.variables.get(data, Variable("", "", ""))
            data = var2.data

        op: str = str(data)
        try:
            while self.full_tokens[counter][0] == self.full_tokens[counter + 1][0]:
                counter += 1
                string: str = self.tokens[counter]
                if self.tokens[counter] not in self.variables and self.tokens[counter].count(
                        '"') == 3:
                    string = self.tokens[counter][1:]
                elif self.tokens[counter].replace('"', '') in self.variables and self.tokens[counter].count('"') != 2:
                    string = self.variables.get(
                        self.tokens[counter].replace(
                            '"', ''), Variable(
                            "", "", "")).data
                op += str(string)

        except IndexError as e:
            print(e)

        if '+' in list(op) or var.var_type != 'str':
            data = eval(op)

        match var.var_type:

            case "int":
                var.data = int(data)
            case "float":
                var.data = float(data)
            case "str":
                var.data = str(data)
            case "bool":
                var.data = bool(data)

        return counter

    def handle_comment(self, i: int) -> int:
        counter: int = i
        if self.tokens[counter] == "/":
            line = self.full_tokens[counter][0]
            while self.full_tokens[counter][0] == line:
                counter += 1
            return counter - 1
        else:
            raise

    def handle_conditional(self, i: int) -> int:
        counter: int = i
        condition: str = ""
        while self.full_tokens[counter][0] == self.full_tokens[counter +
                                                               1][0] or self.tokens[counter] != "{":
            condition += self.tokens[counter]
            counter += 1

        condition = condition.replace('if', '')
        conditionList = list(condition)

        for i, tkn in enumerate(conditionList):
            if tkn in self.variables:
                conditionList[i] = str(
                    self.variables.get(
                        tkn, Variable(
                            "", "", "")).data)

        condition = "".join(conditionList)
        print(condition)

        if eval(condition):
            start: int = counter
            end: int = counter
            # code to execute
            while self.tokens[counter] != '}':
                print(self.tokens[counter])
                counter += 1
                end += 1
            counter = end
            # code to skip
            if self.tokens[counter] == "}":
                counter += 1
            while self.tokens[counter] == "else":
                while self.tokens[counter] != "}":
                    counter += 1
                counter += 1

            print(condition)
            print(counter)
            return counter - 1
        return counter

    def handle_else(self, i: int) -> int:
        if self.tokens[i + 1] == "{":
            # execute code
            ...
        elif self.tokens[i + 1] != "if":
            return i
        else:
            assert False, "Else syntax error"
        return i

    def handle_for(self, i: int) -> int:
        counter: int = i + 1
        index_name: str = ""
        index_start: str | int = ''
        index_end: str | int = ''
        if self.tokens[counter].isalnum() and self.tokens[counter + 1] == '=':

            index_name = self.tokens[counter]
            counter += 2
            if self.tokens[counter].isnumeric():
                index_start = int(self.tokens[counter])
            elif self.tokens[counter] in self.variables:
                index_start = self.variables.get(
                    self.tokens[counter], Variable("", "", "")).data

            counter += 1

            if self.tokens[counter] == 'to':
                counter += 1
            if self.tokens[counter].isnumeric():
                index_end = int(self.tokens[counter])
            elif self.tokens[counter] in self.variables:
                index_end = self.variables.get(
                    self.tokens[counter], Variable("", "", "")).data

        if not str(index_start).isnumeric():
            assert False, "index cannot be a string"
        if not str(index_end).isnumeric():
            assert False, "index cannot be a string"

        print(
            f'index name : {index_name} index start {index_start}  index end {index_end}')
        return counter

    def handle_while(self, i: int) -> int:
        counter: int = i
        condition: str = ""
        while self.full_tokens[counter][0] == self.full_tokens[counter +
                                                               1][0] or self.tokens[counter] != '{':

            condition += self.tokens[counter]
            counter += 1

        condition = condition.replace('while', '')
        print('fine while',)
        return counter

    def handle_function(self, i: int) -> int:
        return i 

    def handle_struct(self, i: int) -> int:
        return i

    def parser(self) -> None:
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]

            if token == "let":
                i = self.handle_declaration(i, False)
            elif token == "const":
                i = self.handle_declaration(i, True)
            elif token in self.variables:
                i = self.handle_var_assignment(i)
            elif token == "/":
                i = self.handle_comment(i)
            elif token == "if":
                i = self.handle_conditional(i)
            elif token == "for":
                i = self.handle_for(i)
            elif token == "while":
                i = self.handle_while(i)
            elif token not in keywords:
                self.tkns_not_recognised.append(token)

            i += 1

