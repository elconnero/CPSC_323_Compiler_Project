#Students    : Darren Chen     
#              Mariah Salgado
# Team Leader: Conner Robbins
#Class       : CPSC-323-07 13801
#Professor   : James S. Choi, Ph.D.
#Date        : 20250212
#Due         : 20250302
#Assignment  : 1

from collections import deque

#Global Variables:
#               0       1      2       3         4       5         6       7          8          9
keywords = {"integer", "if", "else", "endif", "while", "return", "scan", "print", "function", "scan"}
#             0    1    2    3    4   5   6 
seperator = {",", "$", "(", ")", ";","{","}","."}
#            0    1    2    3    4    5    6    7
operator = {"+", "-", "*", "/", "%", "<", ">", "=",}
#            0     1
comment = {"[*", "*]"}

#Function Libs
def user_input ():
    string_check =False
    user_string = input("Enter what you would like to say.\nEnter Here: ")
    while not string_check:
        #if user_string.lstrip().startswith("$$"): # Most likely a starting point, I think it can be replaced with the seperator function and we can figure out how to do a check with that. 
        if len(user_string) != 0: #I do not think we need if statement above, however, this is not a good if statement either and will need to be changed out. 
            string_check = True
        else:
            user_string = input("Error #1:\nCode needs to start with $$ to begin compile.\nEnter what you would like to say.\nEnter Here: ")
    return user_string

def token_giver(code):
        types = {1: "KEYWORD", 2: "OPERATOR", 3: "SEPARATOR", 4: "UNDEFINED"}
        return types.get(code, "UNKNOWN")


def queue_hub(user_input):
    
    # Vars. for this function
    token = ""
    token_queue = deque()

    # Creating queue to put user_string in
    queue = deque(user_input.strip())

    # Process characters from the queue
    while queue:
        char = queue.popleft()  # Get the first character from the queue
        if char == " " or char in seperator or char in operator:
            if token:
                if token in keywords:                                                   
                    token_queue.append((token, token_giver(1)))                  
                else:
                    token_queue.append((token, token_giver(4)))                  
                    token = ""  
            if char in operator:
                token_queue.append((char, token_giver(2)))                  
            elif char in seperator: #Gonna need to get more in depth I fear. 
                token_queue.append((char, token_giver(3)))                  
        else:
            token += char                                                 # Adds character to current token

    # Print the last token if there is one left
    if token:
        if token:
            if token in keywords:                                                   
                token_queue.append((token, token_giver(1)))                  
            else:
                token_queue.append((token, token_giver(4)))                  
                token = ""               
    else:
        token += char 
    
    array = list(token_queue)


def main():
    users_input = user_input()
    lex_hub(users_input)

if __name__ ==  "__main__":
    main()

