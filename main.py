#Students    : Darren Chen     
#              Mariah Salgado
#              Affan Siddiqui
# Team Leader: Conner Robbins
#Class       : CPSC-323-07 13801
#Professor   : James S. Choi, Ph.D.
#Date        : 20250212
#Due         : 20250302
#Assignment  : 1

from collections import deque

# Global Variables:
reserved_words = {
    #               0         1      2       3         4       5         6       7          8         9        10
    "keywords": ["integer", "if", "else", "endif", "while", "return", "scan", "print", "function", "scan", "endwhile"],
    #              0    1    2    3    4    5    6    7 
    "seperator": [",", "$", "(", ")", ";", "{", "}", "."],
    #             0    1    2    3    4    5    6    7    8
    "operator": ["+", "-", "*", "/", "%", "<", ">", "=", "&"],
    #            0     1
    "comment": ["[*", "*]"]
}

files = [
    "source_rat25s.txt",
    "testcase1.txt",
    "testcase2.txt",
    "entermanuel.txt"
]

# =========================
# Function Libs
# =========================

def user_selection(x):
    if x==1:
        for i in range(len(files)):
            print(f'{i}. {files[i]}')

        while True:
            try:
                user_input = int(input ("Enter the file number you would like to test.\nEnter here: "))
                if 0<= user_input <len(files):
                    if user_input <len(files)-1:
                        return files[user_input]
                    else:
                        return "entermanuel.txt"
                else:
                    print(f"Please enter a number between 0 and {len(files) - 1}.")
            except ValueError:
                print("Invalid input. Input a valid number.\nEnter here:")




# Reads source code from a file (source_rat25s.txt)
def read_source_file(filename):
    if filename == "entermanuel.txt":
        user_code = input("Enter the code that you would like to input.\n Enter Here")
        return user_code
    try:
        with open(filename, "r") as f:
            code = f.read()
        return code
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please ensure the file exists.")
        exit(1)

# Returns token type based on a code number.
def token_giver(code):
    types = {1: "KEYWORD", 2: "OPERATOR", 3: "SEPARATOR", 4: "UNDEFINED"}
    return types.get(code, "UNKNOWN")

# Updated queue_hub function that tokenizes the input.
# This version includes a fix so that a dot ('.') is appended to a number token
# if it appears between digits (e.g., "23.00" stays as one token).
def queue_hub(user_input):
    token = ""
    token_queue = deque()
    # Create a queue of characters from the input string.
    queue = deque(user_input.strip())

    while queue:
        char = queue.popleft()

        # Skip Comments
        if char == "[" and queue and queue[0] == "*":
            # Skip the '*'
            queue.popleft()  

            # Continue popping until the end of the comment is found
            while queue:
                next_char = queue.popleft()
                if next_char == "*" and queue and queue[0] == "]":
                    # Skip the closing ']'
                    queue.popleft()  
                    break
            token = ""
            continue

        if char == "\n":
            continue
        
        # Modification: If the current character is a dot, check if it should be part of a number.
        if char == ".":
            # If we already have a token that is all digits and the next character (if any) is also a digit,
            # then the dot is part of a real number.
            if token and token.isdigit() and len(queue) > 0 and queue[0].isdigit():
                token += char
                continue
            # Otherwise, treat the dot as a separator (handled below).

        # If the character is whitespace, or a reserved separator (other than our special handling for dot)
        # or an operator, then finalize the current token.
        if char == " " or (char in reserved_words["seperator"] and char != ".") or char in reserved_words["operator"]:
            if token:
                if token in reserved_words["keywords"]:
                    token_queue.append((token, token_giver(1)))
                else:
                    token_queue.append((token, token_giver(4)))
                token = ""
            # Now handle the reserved character.
            if char in reserved_words["operator"]:
                token_queue.append((char, token_giver(2)))
            elif char in reserved_words["seperator"]:
                token_queue.append((char, token_giver(3)))
        else:
            # Otherwise, add the character to the current token.
            token += char

    # Append any token remaining after the loop.
    if token:
        if token in reserved_words["keywords"]:
            token_queue.append((token, token_giver(1)))
        else:
            token_queue.append((token, token_giver(4)))
    return list(token_queue)

# Combines adjacent operator tokens (for multi-character operators like "<=")
def operator_smasher(token_list):
    x = 0
    while x < len(token_list) - 1:
        if token_list[x][1] == 'OPERATOR' and token_list[x+1][1] == 'OPERATOR':
            smash = token_list[x][0] + token_list[x+1][0]
            token_list[x] = (smash, 'OPERATOR')
            del token_list[x+1]
        else:
            x += 1
    return token_list

# =========================
# FSM for Identifiers
# =========================
class id_fsm:
    def __init__(self):
        self.status = {
            "crossroad": self.crossroad,
            "digit": self.found_digit,
            "letter": self.found_letter,
            "underScore": self.found__,
            "id": self.id_found
        }
        self.current_state = "crossroad"

    def transition(self, char, index, element_len):
        if self.current_state in self.status:
            return self.status[self.current_state](char, index, element_len)
        return False

    def crossroad(self, char, index, element_len):
        if index == 0:
            if char.isalpha():
                self.current_state = "letter"
                return True
            return False
        if char.isalpha():
            self.current_state = "letter"
            return True
        elif char.isdigit():
            self.current_state = "digit"
            return True
        elif char == "_":
            self.current_state = "underScore"
            return True
        else:
            return False

    def found_digit(self, char, index, element_len):
        self.current_state = "id"
        return True

    def found_letter(self, char, index, element_len):
        self.current_state = "id"
        return True

    def found__(self, char, index, element_len):
        self.current_state = "id"
        return True

    def id_found(self, char, index, element_len):
        if index >= element_len:
            return True
        return self.crossroad(char, index, element_len)

# =========================
# FSM for Integers (one or more digits)
# =========================
class int_fsm:
    def process(self, token):
        if not token:
            return False
        for char in token:
            if not char.isdigit():
                return False
        return True

# =========================
# FSM for Reals (digits, a dot, then digits)
# =========================
class real_fsm:
    def process(self, token):
        if not token:
            return False
        state = 0  # 0: reading integer part; 1: dot encountered; 2: reading fractional part.
        for char in token:
            if state == 0:
                if char.isdigit():
                    state = 0
                elif char == '.':
                    state = 1
                else:
                    return False
            elif state == 1:
                if char.isdigit():
                    state = 2
                else:
                    return False
            elif state == 2:
                if not char.isdigit():
                    return False
        # A valid real number must have digits after the dot.
        return state == 2

# =========================
# Token Refinement (lex_hub)
# =========================
def lex_hub(token_record):
    refined_tokens = []
    for tok, tok_type in token_record:
        if tok_type == "UNDEFINED":
            if tok[0].isalpha():
                fsm = id_fsm()
                valid = True
                for idx, char in enumerate(tok):
                    if not fsm.transition(char, idx, len(tok)):
                        valid = False
                        break
                if valid:
                    if tok in reserved_words["keywords"]:
                        refined_tokens.append((tok, "KEYWORD"))
                    else:
                        refined_tokens.append((tok, "IDENTIFIER"))
                else:
                    refined_tokens.append((tok, "ERROR"))
            elif tok[0].isdigit():
                if '.' in tok:
                    fsm = real_fsm()
                    if fsm.process(tok):
                        refined_tokens.append((tok, "REAL"))
                    else:
                        refined_tokens.append((tok, "ERROR"))
                else:
                    fsm = int_fsm()
                    if fsm.process(tok):
                        refined_tokens.append((tok, "INTEGER"))
                    else:
                        refined_tokens.append((tok, "ERROR"))
            else:
                refined_tokens.append((tok, "ERROR"))
        else:
            refined_tokens.append((tok, tok_type))
    return refined_tokens

# =========================
# lexer Function (Generator)
# =========================
def lexer(token_list):
    for token in token_list:
        yield token

# =========================
# Main Function
# =========================
def main():

    # Letting user check which testcase they would like or enter manuel code.
    intake = user_selection(1)

    # Read source code from file.
    source_code = read_source_file(intake)
    
    # Tokenize the input.
    token_record = queue_hub(source_code)
    
    # Combine adjacent operator tokens.
    token_record = operator_smasher(token_record)
    
    # Refine tokens using FSMs.
    refined_tokens = lex_hub(token_record)
    
    # Write tokens to output file.
    outtake = intake.rsplit(".",1)[0] + "_output" + intake.rsplit(".",1)[1]
    with open(outtake, "w") as output_file:
        output_file.write("Token\t\tLexeme\n")
        for token in refined_tokens:
            output_file.write(f"{token[1]:<10}\t{token[0]}\n")
    
    # Also print tokens to the console.
    for token in refined_tokens:
        print(f"{token[1]:<10}\t{token[0]}")
    
    # Demonstrate the lexer() generator.
    print("\nTokens using lexer() generator:")
    token_generator = lexer(refined_tokens)
    for tok in token_generator:
        print(tok)

if __name__ == "__main__":
    main()