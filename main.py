# Students    : Darren Chen     
#               Mariah Salgado
#               Affan Siddiqui
# Team Leader : Conner Robbins
# Class       : CPSC-323-07 13801
# Professor   : James S. Choi, Ph.D.
# Date        : None
# Due         : None
# Assignment  : None
# Main file where all .py's meet. 

import lexar_component, syntax, file_read

def main():

    lexar = lexar_component.lexar_call

    test = lexar("<")
    print(test)

    hello = file_read.file_read()
    test = lexar(hello)
    print(test)


if __name__ == "__main__":
    main()