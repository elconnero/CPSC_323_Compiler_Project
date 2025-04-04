# Students    : Darren Chen     
#               Mariah Salgado
#               Affan Siddiqui
# Team Leader : Conner Robbins
# Class       : CPSC-323-07 13801
# Professor   : James S. Choi, Ph.D.
# Date        : 20250220
# Due         : 20250406
# Assignment  : 2

import lexar_component
import syntax
import file_read
import os

def main():
    print("CPSC 323 Compiler Project Assignment 2 Syntax Analyzer")
    print("4 files that can be tested. If you would like to use your own file, select int(5) below.\n")

    files = [
        "source_rat25s.txt",
        "testcase1.txt",
        "testcase2.txt",
        "me1.txt"
    ]

    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")
    print("5. enter manuel file name")

    while True:
        try:
            selection = int(input("Enter the number next to file name you would like to test.\nEnter here: "))
            if 1 <= selection <= 5:
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Try again.")

    if selection == 5:
        filename = input(
            "Ensure file you wish to analyze is in the same folder as main.py, "
            "furthermore ensure the filename is as exactly as it is in explorer.\n"
            "Example[sample_test_case.txt]\n"
            "Enter the name of the file you wish to bring into program.\nEnter Here: "
        )
    else:
        filename = files[selection - 1]

    # === Lexer ===
    with open(filename, "r") as f:
        source_code = f.read()

    tokens = lexar_component.lexar_call(source_code)

    # Create lexer output file
    lexer_output_filename = os.path.splitext(filename)[0] + "_lexer_output.txt"
    with open(lexer_output_filename, "w") as out_file:
        out_file.write("Token\t\tLexeme\n")
        for token in tokens:
            out_file.write(f"{token[1]:<10}\t{token[0]}\n")
    
    print(f"Lexer output written to: {lexer_output_filename}")

    # === Parser ===
    syntax.run_parser_with_tokens(tokens, filename)

if __name__ == "__main__":
    main()
