# Students    : Darren Chen     
#               Mariah Salgado
#               Affan Siddiqui
# Team Leader : Conner Robbins
# Class       : CPSC-323-07 13801
# Professor   : James S. Choi, Ph.D.
# Date        : 20250220
# Due         : 20250406
# Assignment  : 2

import lexar_component, syntax, file_read

def main():

    # Get the source code using file_read module
    filename = file_read.user_selection()                                       # This is where user will make selection on what type of file they wish to select. 
    source_code = file_read.read_source_file(filename)                          # Once selected, .txt file will get sent back to actually read file. 

    # === Lexer ===
    tokens = lexar_component.lexar_call(source_code)                            # Get list of tokens and what not. 
    type(tokens)

    # Create lexer output file in the same directory as the input file
    #Outputting file
    file_read.file_output(1,filename, tokens)
 
     # === Syntax ===
    TFswitch, output_filename = syntax.run_parser_with_tokens(tokens, filename)

    print(f"Syntax analyzer result  : {TFswitch}")
    print(f"Parser output written to: {output_filename}")

    

if __name__ == "__main__":
    main()
