# Students    : Darren Chen     
#               Mariah Salgado
#               Affan Siddiqui
# Team Leader : Conner Robbins
# Class       : CPSC-323-07 13801
# Professor   : James S. Choi, Ph.D.
# Date        : 20250220
# Due         : 20250510
# Assignment  : 3

import lexar_component
import syntax
import file_read
import os
import sys
from utils import get_base_dir

def main():

    # Get the source code using file_read module
    filename = file_read.user_selection()                                       # This is where user will make selection on what type of file they wish to select. 
    source_code = file_read.read_source_file(filename)                          # Once selected, .txt file will get sent back to actually read file. 

    # === Lexer ===
    tokens = lexar_component.lexar_call(source_code)                            # Get list of tokens and what not. 

    # Create lexer output file in the same directory as the input file
    base_dir = get_base_dir()

    #Outputting file
    file_read.file_output(1,filename, tokens)

    
    syntax.run_parser_with_tokens(tokens, filename)

if __name__ == "__main__":
    main()
