#new
import sys
import os
from lexar_component import user_selection, read_source_file, queue_hub, lexer, operator_smasher
from utils import get_base_dir
from symbol_table import symbol_table
from IGC import InstructionList

# Global variables
current_token = None
current_lexeme = None
token_index = 0
tokens = []
result = True
codegen: InstructionList

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
    if token_index < len(tokens):                                         #  tokens[token_index][1], ""[0]
        current_token, current_lexeme = tokens[token_index][1], tokens[token_index][0]  # (example, "IDENTIFIER")
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
    global result
    print(f"Syntax Error: Expected {expected}, but found {current_token} ('{current_lexeme}')")
    result = False
    exit(1)

# Start symbol for RAT25S grammar
def parseRat25S():
    global result
    print("<Rat25S> -> $$ <Opt Declaration List> $$ <Statement List> $$")
    match('SEPARATOR') 

    parseOptDeclarationList()
    match('SEPARATOR')  

    parseStatementList()
    match('SEPARATOR')  

    if result == True:
        return result
    else:
        return result

def run_parser_with_tokens(tok_list, filename):
    global tokens, token_index, current_token, current_lexeme, codegen

    tokens = tok_list
    tokens.append(('EOF', 'EOF'))
    token_index = 0
    current_token = None
    current_lexeme = None

    # 2) create the emitter
    codegen = InstructionList()

    next_token()  # prime the first token

    # prepare your output file
    base_dir = get_base_dir()
    output_filename = os.path.join(
        base_dir,
        os.path.splitext(os.path.basename(filename))[0] + "_parser_output.txt"
    )

    # 3) redirect stdout for _everything_ you want in that file:
    with open(output_filename, "w") as f:
        sys.stdout = f

        # a) run the parser (which now calls codegen.emit internally)
        result = parseRat25S()

        # b) dump the assembled code
        codegen.dump()

        # c) finally, dump your symbol table
        symbol_table.print_table()

        # restore
        sys.stdout = sys.__stdout__

    return result, output_filename

def parseOptDeclarationList():
    if debug:
        print("<Opt Declaration List> -> <Declaration List> | epsilon")
    
    if current_lexeme in ["integer", "boolean"]:  # Removed "real" as per simplified version
        parseDeclarationList()
    else:
        if debug:
            print("<Opt Declaration List> -> epsilon")

def parseQualifier():
    if debug:
        print("<Qualifier> -> integer | boolean")  # Removed real
    if current_lexeme in ['integer', 'boolean']:  # Removed real
        match('KEYWORD')
    else:
        syntax_error("Qualifier (integer, boolean) expected")

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
            print("<Function Definitions Prime> -> epsilon")

def parseFunction():
    if debug:
        print("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
    
    match('KEYWORD')  # function
    match('Identifier')
    match('SEPARATOR')  # (
    parseOptParameterList()
    match('SEPARATOR')  # )
    parseOptDeclarationList() #TC
    parseBody()

def parseOptParameterList():
    if debug:
        print("<Opt Parameter List> -> <Parameter List> | epsilon")

    if current_token == 'Identifier':
        parseParameterList()
    else:
        if debug:
            print("<Opt Parameter List> -> epsilon")

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
            print("<Parameter List Prime> -> epsilon")

def parseParameter():
    if debug:
        print("<Parameter> -> <Identifier> <Qualifier>")
    match('Identifier')
    parseQualifier()

def parseIDs(type_name, is_declaration=True):
    if debug:
        print("<IDs> -> <Identifier> <IDs Prime>")
    if is_declaration:
        # Insert the identifier into symbol table
        success, error = symbol_table.insert(current_lexeme, type_name)
        if not success:
            print(f"Error: {error}")
            syntax_error("Duplicate identifier")
    else:
        # Check if identifier exists
        addr, type_info = symbol_table.lookup(current_lexeme)
        if addr is None:
            print(f"Error: Variable '{current_lexeme}' not declared")
            syntax_error("Undeclared identifier")
    match('Identifier')
    parseIDsPrime(type_name, is_declaration)

def parseIDsPrime(type_name, is_declaration=True):
    if current_lexeme == ',':
        if debug:
            print("<IDs Prime> -> , <Identifier> <IDs Prime>")
        match('SEPARATOR')  # ,
        if is_declaration:
            # Insert the next identifier into symbol table
            success, error = symbol_table.insert(current_lexeme, type_name)
            if not success:
                print(f"Error: {error}")
                syntax_error("Duplicate identifier")
        else:
            # Check if identifier exists
            addr, type_info = symbol_table.lookup(current_lexeme)
            if addr is None:
                print(f"Error: Variable '{current_lexeme}' not declared")
                syntax_error("Undeclared identifier")
        match('Identifier')     
        parseIDsPrime(type_name, is_declaration)
    else:
        if debug:
            print("<IDs Prime> -> epsilon")

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
            print("<Statement List Prime> -> epsilon")

def parseStatement():
    if debug:
        print("<Statement> -> <Assign> | <If> | <While> | <Return> | <Scan> | <Print> | <Block>")
    if current_token == 'Identifier':
        parseAssign()
    elif current_token == 'KEYWORD':
        if current_lexeme in ('if', 'else', 'endif'):
            #print(f"Why God | current lexeme = {current_lexeme} , current token = {current_token}")
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
    
    # Get the target variable's address
    target_var = current_lexeme
    target_addr, _ = symbol_table.lookup(target_var)
    if target_addr is None:
        syntax_error(f"Undeclared identifier '{target_var}'")
    match('Identifier')
    match('OPERATOR')  # =
    
    # Parse the expression which will leave its result on the stack
    parseExpression()
    
    # Pop the result into the target variable
    codegen.emit('POPM', target_addr)
    
    match('SEPARATOR')  # ;

def parseIf():
    if debug:
        print("<If> -> if ( <Condition> ) <Statement> endif")
    
    if current_lexeme == 'if':
        match('KEYWORD')  # if
        match('SEPARATOR')  # (
        parseCondition()
        match('SEPARATOR')  # )
        parseStatement()
    elif current_lexeme == 'else':
        match('KEYWORD')  # else
        parseStatement()
    else:
        match('KEYWORD')  # endif

def parseElse():
    if debug:
        print("")

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
    if current_token == "SEPARATOR" and current_lexeme == ";":
        match('SEPARATOR')
    else:
        parseExpression()
        codegen.emit('RET')
        match('SEPARATOR')  # ;

def parseScan():
    if debug:
        print("<Scan> -> scan ( <IDs> ) ;")

    # match the "scan" keyword and the "("
    match('KEYWORD')    # scan
    match('SEPARATOR')  # (

    # --- handle the first identifier ---
    identifier = current_lexeme
    addr, _ = symbol_table.lookup(identifier)
    if addr is None:
        syntax_error(f"Undeclared identifier '{identifier}'")
    match('Identifier')
    codegen.emit('READ', addr)

    # --- handle any additional comma-separated IDs ---
    while current_lexeme == ',':
        match('SEPARATOR')  # consume ','
        identifier = current_lexeme
        addr, _ = symbol_table.lookup(identifier)
        if addr is None:
            syntax_error(f"Undeclared identifier '{identifier}'")
        match('Identifier')
        codegen.emit('READ', addr)

    # match the ")" and the trailing ";"
    match('SEPARATOR')  # )
    match('SEPARATOR')  # ;

def parsePrint():
    if debug:
        print("<Print> -> print ( <IDs> ) ;")
    match('KEYWORD')  # print
    match('SEPARATOR')  # (
    parseExpression()  
    codegen.emit('WRITE')
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
        op = current_lexeme
        match('OPERATOR')
        parseTerm()
        # Emit the appropriate arithmetic operation
        if op == '+':
            codegen.emit('A')  # Add
        else:
            codegen.emit('S')  # Subtract
        parseExpressionPrime()
    else:
        if debug:
            print("<Expression Prime> -> epsilon")

def parseTerm():
    if debug:
        print("<Term> -> <Factor> <Term Prime>")
    parseFactor()
    parseTermPrime()

def parseTermPrime():
    if current_lexeme in ['*', '/']:
        if debug:
            print("<Term Prime> -> * <Factor> <Term Prime> | / <Factor> <Term Prime>")
        op = current_lexeme
        match('OPERATOR')
        parseFactor()
        # Emit the appropriate arithmetic operation
        if op == '*':
            codegen.emit('M')  # Multiply
        else:
            codegen.emit('D')  # Divide
        parseTermPrime()
    else:
        if debug:
            print("<Term Prime> -> epsilon")

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
        # look up the address in the symbol table
        addr, _ = symbol_table.lookup(current_lexeme)
        if addr is None:
            print(f"Error: Variable '{current_lexeme}' not declared")
            syntax_error("Undeclared identifier")
        # emit a PUSHM for this variable
        codegen.emit('PUSHM', addr)
        match('Identifier')
        parsePrimaryPrime()

    elif current_token == 'Integer':
        # emit a PUSHI for the literal value
        codegen.emit('PUSHI', int(current_lexeme))
        match('Integer')

    elif current_token == 'Real':
        # real not allowed in simplified version
        syntax_error("Real numbers not allowed in simplified version")

    elif current_lexeme in ('true', 'false'):
        # for booleans you might choose to push 1/0
        val = 1 if current_lexeme == 'true' else 0
        codegen.emit('PUSHI', val)
        match('KEYWORD')

    elif current_lexeme == '(':
        match('SEPARATOR')  # (
        parseExpression()
        match('SEPARATOR')  # )

    else:
        syntax_error("Invalid primary")

def parsePrimaryPrime():
    if current_lexeme == '(':
        if debug:
            print("<Primary Prime> -> ( <IDs> )")
        match('SEPARATOR')
        parseIDs("integer")  # Function parameters are always integers in simplified Rat24S
        match('SEPARATOR')
    else:
        if debug:
            print("<Primary Prime> -> epsilon")

def parseDeclarationList():
    if debug:
        print("<Declaration List> -> <Declaration> ; <Declaration List Prime>")
    parseDeclaration()
    match('SEPARATOR')  # ;
    parseDeclarationListPrime()

def parseDeclarationListPrime():
    if current_lexeme in ["integer", "boolean"]:  # Removed real
        if debug:
            print("<Declaration List Prime> -> <Declaration> ; <Declaration List Prime>")
        parseDeclaration()
        match('SEPARATOR')  # ;
        parseDeclarationListPrime()
    else:
        if debug:
            print("<Declaration List Prime> -> epsilon")

def parseDeclaration():
    if debug:
        print("<Declaration> -> <Qualifier> <IDs>")
    type_name = current_lexeme  # Store the type before parsing
    parseQualifier()
    parseIDs(type_name)