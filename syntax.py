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
        "<Rat25S> ::= $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$",            #0   R1        
        "<Opt Function Definitions> ::= <Function Definitions> | <Empty>",                                        #1   R2 
        "<Function Definitions> ::= <Function> | <Function> <Function Definitions Prime>",                        #2   R3
        "<Function Definitions Prime> ::= ε | <Function Definitions>",                                            #3   R4
        "<Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>",            #4   R5 
        "<Opt Parameter List> ::= <Parameter List> | <Empty>",                                                    #5   R6                                    
        "<Parameter List> ::= <Parameter> | <Parameter> , <Parameter List Prime>",                                #6   R7
        "<Parameter List Prime> ::= ε | , <Parameter List>",                                                      #7   R8
        "<Parameter> ::= <IDs> <Qualifier>",                                                                      #8   R9  
        "<Qualifier> ::= integer | boolean | real",                                                               #9   R10 
        "<Body> ::= { <Statement List> }",                                                                        #10  R11  
        "<Opt Declaration List> ::= <Declaration List> | <Empty>",                                                #11  R12  
        "<Declaration List> := <Declaration> ; | <Declaration> <Declaration List Prime>",                         #12  R13
        "<Declaration List Prime> ::= ε | <Declaration List>",                                                    #13  R14
        "<Declaration> ::= integer <IDs> | boolean <IDs> | real <IDs>",                                           #14  R15  
        "<IDs> ::= <Identifier> | <Identifier><IDs Prime>",                                                       #15  R16
        "<IDs Prime> ::= ε | , <IDs>",                                                                            #16  R17
        "<Statement List> ::= <Statement> | <Statement><Statement List Prime>",                                   #17  R18
        "<Statement List Prime> ::= ε | <Statement List>",                                                        #18  R19
        "<Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>",                   #19  R20 
        "<Compound> ::= { <Statement List> }",                                                                    #20  R21  
        "<Assign> ::= <Identifier> = <Expression>",                                                               #21  R22  
        "<If> ::= if ( <Condition> ) <Statement><If Prime>",                                                      #22  R23
        "<If Prime> ::= endif | else <Statement> endif",                                                          #23  R24
        "<Return> ::= return ; | return <Return Prime>",                                                          #24  R25
        "<Return Prime> ::= ; | <Expression> ;",                                                                  #25  R26
        "<Print> ::= print ( <Expression> )",                                                                     #26  R27  
        "<Scan> ::= scan ( <IDs> )",                                                                              #27  R28  
        "<While> ::= while ( <Condition> ) <Statement> endwhile",                                                 #28  R29  
        "<Condition> ::= <Expression> <Relop> <Expression>",                                                      #29  R30  
        "<Relop> ::= == | != | > | < | <= | =>",                                                                  #30  R31  
        "<Expression> ::= <Term> <Expression Prime>",                                                             #31  R32  
        "<Expression Prime> ::= + <Term> <Expression Prime> | - <Term> <Expression Prime> | ε",                   #32  R33  
        "<Term> ::= <Factor> <Term Prime>",                                                                       #33  R34  
        "<Term Prime> ::= * <Factor> <Term Prime> | / <Factor> <Term Prime> | ε",                                 #34  R35 
        "<Factor> ::= - <Primary> | <Primary>",                                                                   #35  R36  
        "<Primary> ::= <Identifier> <Primary Prime> | <Integer> | ( <Expression> ) | <Real> | true | false",      #36  R37
        " <Primary Prime> ::= ε | ( <IDs> )",                                                                     #37  R38
        "<Empty> ::= ε",                                                                                          #38  R39  
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

    if token[0] != ('$$', 'SEPARATOR'): 
        return "<ERROR>, $$ MISSING" # I am not sure if this is the right thing to do, but we are going to go forward. 
    token.pop(0)
    
    if token[0] == ('function', 'KEYWORD'):
        OFD(token, flicker)

    if token[0] == None:
        return None # I have this here because OFD and ODL both have an empty option. , The more I think of it, this really might not be the best option. 
    else:
        return "<ERROR>, Lost in EMPTY From R1"

#R2
def OFD(token, flicker): # Opt Function Definitions

    if flicker == 1:
        print(f'{rat_rules(1)} .1')    

    parse_function(token, flicker)

#R3
def FD(token, flicker): #Function Definitions
    if flicker == 1:
        print(rat_rules(2))    
    
#R4
def FD_prime(token, flicker): #Function Definitions Prime
    if flicker == 1:
        print(rat_rules(3))    
    pass

#R5
def parse_function(token, flicker): #function
    if flicker == 1:
        print(rat_rules(4))    

    token.pop(0)
    if token[1] == 'IDENTIFIER':
        if token[0] == ('(', 'SEPARATOR'):
            OPL(token, flicker) # We have a check for ')' if empty at OPL. Make sure we have a backup plan if there are conents within there.

#R6
def OPL(token, flicker): # Opt Parameter List
    if flicker == 1:
        print(rat_rules(5))    
    
    token.pop(0)
    if token[0] == (')', 'SEPARATOR'): #This is my version of empty.
        token.pop(0)
        ODL(token,flicker)

    PL(token, flicker)
    
    


#R7
def PL(token, flicker): #Parameter List
    if flicker == 1:
        print(rat_rules(6))
    pass

    parse_parameter(token, flicker)
    PL_prime(token, flicker)

#R8
def PL_prime(token, flicker): #Parameter List Prime
    if flicker == 1:
        print(rat_rules(7))
    pass

#R9
def parse_parameter(token, flicker): #Parameter
    if flicker == 1:
        print(rat_rules(8))    
    pass
    #This is where you last left off.

#R10
def parse_qualifier(token, flicker): #qualifier
    if flicker == 1:
        print(rat_rules(9))    
    pass

#R11 
def parse_body(token, flicker): #Body
    if flicker == 1:
        print(rat_rules(10))    
    pass

#R12
def ODL(token, flicker): #Opt Decleration List
    if flicker == 1:
        print(rat_rules(11))    
    pass

#R13
def DL(token, flicker): #Decleration List
    if flicker == 1:
        print(rat_rules(12))    
    pass

#R14
def DL_prime(token, flicker): #Decleration List Prime
    if flicker == 1:
        print(rat_rules(13))    
    pass

#R15
def parse_declaration(token, flicker): #Decleration
    if flicker == 1:
        print(rat_rules(14))    
    pass

#R16
def parse_id(token, flicker): #id
    if flicker == 1:
        print(rat_rules(15))    
    pass

#R17
def id_prime(token, flicker): #id Prime
    if flicker == 1:
        print(rat_rules(16))    
    pass

#R18
def SL(token, flicker): #Statelement List
    if flicker == 1:
        print(rat_rules(17))    
    pass

#R19
def SL_prime(token, flicker): #Statelement List Prime
    if flicker == 1:
        print(rat_rules(18))    
    pass

#R20 
def parse_statement(token, flicker): #statement
    if flicker == 1:
        print(rat_rules(19))    
    pass

#R21 
def parse_compound(token, flicker): #compound
    if flicker == 1:
        print(rat_rules(20))    
    pass

#R22
def parse_assign(token, flicker): #Assign
    if flicker == 1:
        print(rat_rules(21))    
    pass

#R23
def parse_if(token, flicker): #if
    if flicker == 1:
        print(rat_rules(22))    
    pass

#R24
def if_prime(token, flicker): #if prime
    if flicker == 1:
        print(rat_rules(23))    
    pass

#R25
def parse_return(token, flicker): #return
    if flicker == 1:
        print(rat_rules(24))    
    pass

#R26
def return_prime(token, flicker): #return Prime
    if flicker == 1:
        print(rat_rules(25))    
    pass

#R27
def parse_print(token, flicker): #return
    if flicker == 1:
        print(rat_rules(26))    
    pass

#R28
def parse_scan(token, flicker): #scan
    if flicker == 1:
        print(rat_rules(27))    
    pass

#R29
def parse_while(token, flicker): #while
    if flicker == 1:
        print(rat_rules(28))    
    pass

#R30
def parse_condition(token, flicker): #condition
    if flicker == 1:
        print(rat_rules(29))    
    pass

#R31 
def parse_relop(token, flicker): #relop
    if flicker == 1:
        print(rat_rules(30))    
    pass

#R32 
def parse_expression(token, flicker): #Expression
    if flicker == 1:
        print(rat_rules(31))    
    pass

#R33
def EP(token, flicker): #Expression Prime
    if flicker == 1:
        print(rat_rules(32))    
    pass

#R34
def parse_term(token, flicker): #Term
    if flicker == 1:
        print(rat_rules(33))    
    pass

#R35
def TP(token, flicker): #Term Prime
    if flicker == 1:
        print(rat_rules(34))    
    pass

#R36
def parse_factor(token, flicker): #factor
    if flicker == 1:
        print(rat_rules(35))    
    pass

#R37
def parse_primary(token, flicker): #primary
    if flicker == 1:
        print(rat_rules(36))    
    pass

#R38
def PP(token, flicker): #primary Prime
    if flicker == 1:
        print(rat_rules(37))    
    pass

#R39
def null(token, flicker): #Empty
    if flicker == 1:
        print(rat_rules(38))    
    pass


# =========================
# END OF PARSE
# =========================


def main():
    
    lexar = lexar_component.lexar_call
    me1 = file_read.syntax_testcase() #Classic testcase to see if this works, can change filename in file_read.py
    token = lexar(me1) # If you wish to modify this to try out different testcases, change file_read.syntax_testcase() in me1 to file_read.file_read()
    light = switch()

    rat25s(token, light)
    print(token,light)

if __name__ == "__main__":
    main()



# Notes:
# <Error> Is just something I thought we can use to check