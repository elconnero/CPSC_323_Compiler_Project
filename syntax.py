#Students    : Darren Chen     
#              Mariah Salgado
#              Affan Siddiqui
# Team Leader: Conner Robbins
#Class       : CPSC-323-07 13801
#Professor   : James S. Choi, Ph.D.
#Date        : 20250220
#Due         : 20250406
#Assignment  : 2

import lexar_component, file_read


# Global Variables:
# switch = None # We might just have a user change this to true or false here, it would be interesting to do it this way. // Also might just keep this in troubleshoot

# =========================
# Function Libs
# =========================

def switch():
    light = None
    while True:
        try:
            user_input = int(input("Would you like to print debug flags while Syntax Analyxer conducts its work?\n1. No\n2. Yes\nType in corresponding integer next to statement.\nEnter Here: "))
            if 1 <= user_input <= 2:
                light = user_input - 1
                return light
        except ValueError:
            print("Enter 1 for NO.\nEnter 2 for YES.")


def main():
    
    lexar = lexar_component.lexar_call
    hello = file_read.syntax_testcase()
    test = lexar(hello)
    light = switch()




    print(test,light)

if __name__ == "__main__":
    main()



# Notes:
# The parser should print to an output file the tokens, lexemes and
# the production rules used.