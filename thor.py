#!/usr/bin/env python3
import os
import sys
from interpreter.lexer import Lexer
from interpreter.parser import Parser
# from Clibrary.lib import clibrary

version: str = "0.7.0"

def help_message():
    print()

def cli() -> str:
    if len(sys.argv) >= 1:
        match sys.argv[1]:
            case '--help':
                print(f'help')
            case '--version' | '-v':
                print(f'Version: {version}')
            case _:
                filepath, file_extension = os.path.splitext(sys.argv[1])
                assert file_extension == ".th",f" File Extension should not be: {file_extension}"
                return filepath+file_extension
    else:
        help_message()
    
    return ""

def main():
    filepath= cli()
    lexer = Lexer(filepath)
    parser = Parser(lexer.tokens,lexer.full_tokens)
    # clibrary.print()


if __name__ == "__main__":
    main()
