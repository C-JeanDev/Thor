#!/usr/bin/env python3
import os
import sys
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from Clibrary.lib import clibrary
 

def cli() -> str:
    if len(sys.argv) >= 1:
        match sys.argv[1]:
            case '--help':
                print(f'help')
            case '--version':
                print(f'version')
            case _:
                filepath, file_extension = os.path.splitext(sys.argv[1])
                assert file_extension == ".th",f"File Extension should be  not {file_extension}"
                print(filepath,file_extension)
                return filepath+file_extension
    return "" 


def main():
    filepath= cli()
    lexer = Lexer(filepath)
    parser = Parser(lexer.tokens,lexer.full_tokens)
    # clibrary.print()


if __name__ == "__main__":
    main()
