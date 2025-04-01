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

def rat_rules(rule_number):
    rules = [
        "<Rat25S> ::= $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$",                #0  R1
        "<Opt Function Definitions> ::= <Function Definitions> | <Empty>",                                            #1  R2
        "<Function Definitions> ::= <Function> | <Function> <Function Definitions>",                                  #2  R3
        "<Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>",                #3  R4
        "<Opt Parameter List> ::= <Parameter List> | <Empty>",                                                        #4  R5                                        
        "<Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>",                                          #5  R6
        "<Parameter> ::= <IDs> <Qualifier>",                                                                          #6  R7
        "<Qualifier> ::= integer | boolean | real",                                                                   #7  R8
        "<Body> ::= { <Statement List> }",                                                                            #8  R9
        "<Opt Declaration List> ::= <Declaration List> | <Empty>",                                                    #9  R10
        "<Declaration List> := <Declaration> ; | <Declaration> ; <Declaration List>",                                 #10 R11
        "<Declaration> ::= integer <IDs> | boolean <IDs> | real <IDs>",                                               #11 R12
        "<IDs> ::= <Identifier> | <Identifier>, <IDs>",                                                               #12 R13
        "<Statement List> ::= <Statement> | <Statement> <Statement List>",                                            #13 R14
        " <Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>",                      #14 R15
        "<Compound> ::= { <Statement List> }",                                                                        #15 R16
        "<Assign> ::= <Identifier> = <Expression>",                                                                   #16 R17
        "<If> ::= if ( <Condition> ) <Statement> endif | if ( <Condition> ) <Statement> else <Statement> endif",      #17 R18
        "<Return> ::= return ; | return <Expression>",                                                                #18 R19
        "<Print> ::= print ( <Expression> )",                                                                         #19 R20
        "<Scan> ::= scan ( <IDs> )",                                                                                  #20 R21
        "<While> ::= while ( <Condition> ) <Statement> endwhile",                                                     #21 R22
        "<Condition> ::= <Expression> <Relop> <Expression>",                                                          #22 R23
        "<Relop> ::= == | != | > | < | <= | =>",                                                                      #23 R24
        "<Expression> ::= <Term> <Expression Prime>",                                                                 #24 R25
        "<Expression Prime> ::= + <Term> <Expression Prime> | - <Term> <Expression Prime> | ε",                       #25 R26
        "<Term> ::= <Factor> <Term Prime>",                                                                           #26 R27
        "<Term Prime> ::= * <Factor> <Term Prime> | / <Factor> <Term Prime> | ε",                                     #27 R28
        "<Factor> ::= - <Primary> | <Primary>",                                                                       #28 R29
        "<Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) | ( <Expression> ) | <Real> | true | false", #29 R30
        "<Empty> ::= ε",                                                                                              #30 R31
    ]
    return rules[rule_number]

# =========================
# END of Function Libs
# =========================

# =========================
# PARSE
# =========================

#R1
def rat25s(token, flicker):
    if flicker == 1:
        print(rat_rules(0))
    pass

#R2
def OFD(token, flicker): # Opt Function Definitions
    if flicker == 1:
        print(rat_rules(1))    
    pass

#R3
def FD(token, flicker): #Function Definitions
    if flicker == 1:
        print(rat_rules(2))    
    pass

#R4
def parse_function(token, flicker): #function
    if flicker == 1:
        print(rat_rules(3))    
    pass

#R5
def OPL(token, flicker): # Opt Parameter List
    if flicker == 1:
        print(rat_rules(4))    
    pass

#R6
def PL(token, flicker): #Parameter List
    if flicker == 1:
        print(rat_rules(5))    
    pass

#R7
def parse_parameter(token, flicker): #Parameter
    pass

#R8
def parse_qualifier(token, flicker): #qualifier
    pass

#R9 
def parse_body(token, flicker): #Body
    pass

#R10
def ODL(token, flicker): #Opt Decleration List
    pass

#R11
def DL(token, flicker): #Decleration List
    pass

#R12
def parse_declaration(token, flicker): #Decleration
    pass

#R13
def parse_id(token, flicker): #id
    pass

#R14
def SL(token, flicker): #Statelement List
    pass

#R15 
def parse_statement(token, flicker): #statement
    pass

#R16 
def parse_compound(token, flicker): #compound
    pass

#R17
def parse_assign(token, flicker): #Assign
    pass

#R18
def parse_if(token, flicker): #if
    pass

#R19
def parse_return(token, flicker): #return
    pass

#R20
def parse_print(token, flicker): #return
    pass

#R21
def parse_scan(token, flicker): #scan
    pass

#R22
def parse_while(token, flicker): #while
    pass

#R23
def parse_condition(token, flicker): #condition
    pass

#R24 
def parse_relop(token, flicker): #relop
    pass

#R25 
def parse_expression(token, flicker): #Expression
    pass

#R26
def EP(token, flicker): #Expression Prime
    pass

#R27
def parse_term(token, flicker): #Term
    pass

#R28
def TP(token, flicker): #Term Prime
    pass

#R29
def parse_factor(token, flicker): #factor
    pass

#R30
def parse_primary(token, flicker): #primary
    pass

#R31 
def null(token, flicker): #Empty
    pass


# =========================
# END OF PARSE
# =========================


def main():
    
    lexar = lexar_component.lexar_call
    me1 = file_read.syntax_testcase() #Classic testcase to see if this works, can change filename in file_read.py
    token = lexar(me1) # If you wish to modify this to try out different testcases, change file_read.syntax_testcase() in me1 to file_read.file_read()
    light = switch()





    print(token,light)

if __name__ == "__main__":
    main()



# Notes:
# The parser should print to an output file the tokens, lexemes and
# the production rules used.