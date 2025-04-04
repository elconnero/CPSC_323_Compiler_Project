import sys
import os
from lexar_component import user_selection, read_source_file, queue_hub, lexer, operator_smasher# import necessary functions from lexer

# Global variables
current_token = None
current_lexeme = None
token_index = 0
tokens = []

# Debug switch
debug = True

# Load and process the source file into tokens
def load_tokens():
    global tokens
    filename = user_selection() # ask user to select input file
    source_code = read_source_file(filename) # read contents of file
    token_queue = queue_hub(source_code)# break input into  tokens
    token_queue = operator_smasher(token_queue)# combine multi-char operators
    tokens = list(lexer(token_queue))# finalize tokens
    tokens.append(('EOF', 'EOF'))# append end-of-file token

# Move to the next token in the token list
def next_token():
    global current_token, current_lexeme, token_index
    if token_index < len(tokens):
        current_token, current_lexeme = tokens[token_index][1], tokens[token_index][0]
        token_index += 1

# Match the current token with the expected token
def match(expected_token):
    if current_token == expected_token:
        if debug:
            print(f"Matched: Token: {current_token}, Lexeme: {current_lexeme}")
        next_token()
    else:
        syntax_error(expected_token)

# Handle unexpected syntax
def syntax_error(expected):
    print(f"Syntax Error: Expected {expected}, but found {current_token} ('{current_lexeme}')")
    exit(1)

# Start symbol for RAT25S grammar
def parseRat25S():
    print("<Rat25S> -> $$ <Opt Function Definitions> $$ <Opt Declaration List> $$ <Statement List> $$")
    match('SEPARATOR')  
    parseOptFunctionDefinitions()
    match('SEPARATOR')  
    parseOptDeclarationList()
    match('SEPARATOR')  
    parseStatementList()
    match('SEPARATOR')  

def run_parser_with_tokens(tok_list, filename):
    global tokens, token_index, current_token, current_lexeme
    tokens = tok_list
    tokens.append(('EOF', 'EOF'))
    token_index = 0
    current_token = None
    current_lexeme = None

    next_token()

    # Create parser output file
    output_filename = os.path.splitext(filename)[0] + "_parser_output.txt"

    with open(output_filename, "w") as f:
        sys.stdout = f
        parseRat25S()
        sys.stdout = sys.__stdout__ 

    print(f"Parser output written to: {output_filename}")



def parseOptFunctionDefinitions():
    if debug:
        print("<Opt Function Definitions> -> <Function Definitions> | ε")
    
    if current_token == 'KEYWORD' and current_lexeme == 'function':
        parseFunctionDefinitions()
    else:
        if debug:
            print("<Opt Function Definitions> -> ε")  # epsilon (empty)
        return

def parseFunctionDefinitions():
    if debug:
        print("<Function Definitions> -> <Function> <Function Definitions Prime>")
    parseFunction()
    parseFunctionDefinitionsPrime()

def parseFunctionDefinitionsPrime():
    if current_token == 'KEYWORD' and current_lexeme == 'function':
        if debug:
            print("<Function Definitions Prime> -> <Function> <Function Definitions Prime>")
        parseFunction()
        parseFunctionDefinitionsPrime()
    else:
        if debug:
            print("<Function Definitions Prime> -> ε")

def parseFunction():
    if debug:
        print("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
    
    match('KEYWORD')  # function
    match('Identifier')
    match('SEPARATOR')  # (
    parseOptParameterList()
    match('SEPARATOR')  # )
    parseOptDeclarationList()
    parseBody()

def parseOptParameterList():
    if debug:
        print("<Opt Parameter List> -> <Parameter List> | ε")

    if current_token == 'Identifier':
        parseParameterList()
    else:
        if debug:
            print("<Opt Parameter List> -> ε")

def parseParameterList():
    if debug:
        print("<Parameter List> -> <Parameter> <Parameter List Prime>")
    parseParameter()
    parseParameterListPrime()

def parseParameterListPrime():
    if current_lexeme == ',':
        if debug:
            print("<Parameter List Prime> -> , <Parameter> <Parameter List Prime>")
        match('SEPARATOR')
        parseParameter()
        parseParameterListPrime()
    else:
        if debug:
            print("<Parameter List Prime> -> ε")

def parseParameter():
    if debug:
        print("<Parameter> -> <Identifier> <Qualifier>")
    match('Identifier')
    parseQualifier()

def parseQualifier():
    if debug:
        print("<Qualifier> -> integer | boolean | real")
    if current_lexeme in ['integer', 'boolean', 'real']:
        match('KEYWORD')
    else:
        syntax_error("Qualifier (integer, boolean, real) expected")



def parseOptDeclarationList():
    if debug:
        print("<Opt Declaration List> -> <Declaration List> | ε")
    
    if current_lexeme in ["integer", "boolean", "real"]:
        parseDeclarationList()
    else:
        if debug:
            print("<Opt Declaration List> -> ε")

def parseDeclarationList():
    if debug:
        print("<Declaration List> -> <Declaration> ; <Declaration List Prime>")
    parseDeclaration()
    match('SEPARATOR')  # ;
    parseDeclarationListPrime()

def parseDeclarationListPrime():
    if current_lexeme in ["integer", "boolean", "real"]:
        if debug:
            print("<Declaration List Prime> -> <Declaration> ; <Declaration List Prime>")
        parseDeclaration()
        match('SEPARATOR')  # ;
        parseDeclarationListPrime()
    else:
        if debug:
            print("<Declaration List Prime> -> ε")

def parseDeclaration():
    if debug:
        print("<Declaration> -> <Qualifier> <IDs>")
    parseQualifier()
    parseIDs()

def parseIDs():
    if debug:
        print("<IDs> -> <Identifier> <IDs Prime>")
    match('Identifier')
    parseIDsPrime()

def parseIDsPrime():
    if current_lexeme == ',':
        if debug:
            print("<IDs Prime> -> , <Identifier> <IDs Prime>")
        match('SEPARATOR')  # ,
        match('Identifier')
        parseIDsPrime()
    else:
        if debug:
            print("<IDs Prime> -> ε")

def parseBody():
    if debug:
        print("<Body> -> { <Statement List> }")
    match('SEPARATOR')  # {
    parseStatementList()
    match('SEPARATOR')  # }

def parseStatementList():
    if debug:
        print("<Statement List> -> <Statement> <Statement List Prime>")
    parseStatement()
    parseStatementListPrime()

def parseStatementListPrime():
    if current_token in ['Identifier', 'KEYWORD']:
        if debug:
            print("<Statement List Prime> -> <Statement> <Statement List Prime>")
        parseStatement()
        parseStatementListPrime()
    else:
        if debug:
            print("<Statement List Prime> -> ε")



def parseStatement():
    if debug:
        print("<Statement> -> <Assign> | <If> | <While> | <Return> | <Scan> | <Print> | <Block>")
    if current_token == 'Identifier':
        parseAssign()
    elif current_token == 'KEYWORD':
        if current_lexeme == 'if':
            parseIf()
        elif current_lexeme == 'while':
            parseWhile()
        elif current_lexeme == 'return':
            parseReturn()
        elif current_lexeme == 'scan':
            parseScan()
        elif current_lexeme == 'print':
            parsePrint()
        else:
            syntax_error("Expected valid statement keyword")
    elif current_lexeme == '{':
        if debug:
            print("<Statement> -> <Block>")
        parseBody()
    else:
        syntax_error("Expected a statement")

def parseAssign():
    if debug:
        print("<Assign> -> <Identifier> = <Expression> ;")
    match('Identifier')
    match('OPERATOR')  # =
    parseExpression()
    match('SEPARATOR')  # ;

def parseIf():
    if debug:
        print("<If> -> if ( <Condition> ) <Statement> endif")
    match('KEYWORD')  # if
    match('SEPARATOR')  # (
    parseCondition()
    match('SEPARATOR')  # )
    parseStatement()
    match('KEYWORD')  # endif

def parseWhile():
    if debug:
        print("<While> -> while ( <Condition> ) <Statement> endwhile")
    match('KEYWORD')  # while
    match('SEPARATOR')  # (
    parseCondition()
    match('SEPARATOR')  # )
    parseStatement()
    match('KEYWORD')  # endwhile

def parseReturn():
    if debug:
        print("<Return> -> return <Expression> ;")
    match('KEYWORD')  # return
    parseExpression()
    match('SEPARATOR')  # ;

def parseScan():
    if debug:
        print("<Scan> -> scan ( <IDs> ) ;")
    match('KEYWORD')  # scan
    match('SEPARATOR')  # (
    parseIDs()
    match('SEPARATOR')  # )
    match('SEPARATOR')  # ;

def parsePrint():
    if debug:
        print("<Print> -> print ( <IDs> ) ;")
    match('KEYWORD')  # print
    match('SEPARATOR')  # (
    parseIDs()
    match('SEPARATOR')  # )
    match('SEPARATOR')  # ;

def parseCondition():
    if debug:
        print("<Condition> -> <Expression> <Relop> <Expression>")
    parseExpression()
    parseRelop()
    parseExpression()

def parseRelop():
    if debug:
        print("<Relop> -> == | != | > | < | <= | =>")
    if current_lexeme in ['==', '!=', '>', '<', '<=', '=>']:
        match('OPERATOR')
    else:
        syntax_error("Relational operator expected")

def parseExpression():
    if debug:
        print("<Expression> -> <Term> <Expression Prime>")
    parseTerm()
    parseExpressionPrime()

def parseExpressionPrime():
    if current_lexeme in ['+', '-']:
        if debug:
            print("<Expression Prime> -> + <Term> <Expression Prime> | - <Term> <Expression Prime>")
        match('OPERATOR')
        parseTerm()
        parseExpressionPrime()
    else:
        if debug:
            print("<Expression Prime> -> ε")

def parseTerm():
    if debug:
        print("<Term> -> <Factor> <Term Prime>")
    parseFactor()
    parseTermPrime()

def parseTermPrime():
    if current_lexeme in ['*', '/', '%']:
        if debug:
            print("<Term Prime> -> * <Factor> <Term Prime> | / <Factor> <Term Prime> | % <Factor> <Term Prime>")
        match('OPERATOR')
        parseFactor()
        parseTermPrime()
    else:
        if debug:
            print("<Term Prime> -> ε")

def parseFactor():
    if debug:
        print("<Factor> -> - <Primary> | <Primary>")
    if current_lexeme == '-':
        match('OPERATOR')
        parsePrimary()
    else:
        parsePrimary()

def parsePrimary():
    if debug:
        print("<Primary> -> <Identifier> | <Integer> | <Real> | ( <Expression> )")
    if current_token == 'Identifier':
        match('Identifier')
    elif current_token in ['Integer', 'Real']:
        match(current_token)
    elif current_lexeme == '(':
        match('SEPARATOR')
        parseExpression()
        match('SEPARATOR')  # )
    else:
        syntax_error("Expected primary expression")
