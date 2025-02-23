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
reserved_words = {
#               0       1      2       3         4       5         6       7          8          9
"keywords": ["integer", "if", "else", "endif", "while", "return", "scan", "print", "function", "scan"],
#             0    1    2    3    4   5   6 
"seperator":[",", "$", "(", ")", ";","{","}","."],
#            0    1    2    3    4    5    6    7
"operator": ["+", "-", "*", "/", "%", "<", ">", "="],
#            0     1
"comment":["[*", "*]"]
}

#Function Libs
def user_input ():
    string_check =False
    user_string = input("Enter what you would like to say.\nEnter Here: ")
    while not string_check:
        #if user_string.lstrip().startswith("$$"): # Most likely a starting point, I think it can be replaced with the seperator function and we can figure out how to do a check with that. 
        if len(user_string) != 0: #I do not think we need if statement above, however, this is not a good if statement either and will need to be changed out. 
            string_check = True
        else: # Leaving this as while so that we can prepare for the $$ in the future. 
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
        if char == " " or char in reserved_words["seperator"] or char in reserved_words["operator"]:
            if token:
                if token in reserved_words["keywords"]:                                                   
                    token_queue.append((token, token_giver(1)))                  
                else:
                    token_queue.append((token, token_giver(4)))                  
                    token = ""  
            if char in reserved_words["operator"]:
                token_queue.append((char, token_giver(2)))                  
            elif char in reserved_words["seperator"]: #Gonna need to get more in depth I fear. 
                token_queue.append((char, token_giver(3)))                  
        else:
            token += char   # Adds character to current token

    # Print the last token if there is one left
    if token:
        if token:
            if token in reserved_words["keywords"]:                                                   
                token_queue.append((token, token_giver(1)))                  
            else:
                token_queue.append((token, token_giver(4)))                  
                token = ""               
    else:
        token += char 
    
    return list(token_queue)

def operator_smasher(token):
    x = 0
    while x < len(token) -1 :
        if token[x][1] == 'OPERATOR' and token[x+1][1] == 'OPERATOR':
            smash = (token[x][0] + token[x+1][0], 'OPERATOR')
            token[x] = smash
            del token[x+1]
        else:
            x+=1
    return token


    #FSM
class id_fsm:
    def __init__(self):
        self.status = {
            #"first state": self.first_state,# Might not need this here, might make it its own FSM. ## Feeling more confident we might not need because "def transition" sort of does state 1 already.
            "crossroad": self.crossroad,
            "digit": self.found_digit,
            "letter": self.found_letter,
            "underScore": self.found__,
            "id": self.id_found
        }
        self.current_state = "crossroad"

    def transition(self, status, index, element_len): # can we techni // Not sure if needed, but really trying to see if having the len of element will be important to the fsr.
        if self.current_state in self.status:
            return self.status[self.current_state](status, index, element_len)
        return False
        
    def crossroad(self, status, index, element_len):

        if index == 0:
            if status.isalpha():
                return True
            return False

        if status.isalpha():
            self.current_state = "letter"
            return True
        elif status.isdigit():
            self.current_state = "digit"
            return True
        elif status == "_": 
            self.current_state = "underScore"
            return True
        else:
            return False

    def found_digit(self, status, index, element_len):
        self.current_state = "id"
        return True

    def found_letter(self, status, index, element_len):
        self.current_state = "id"
        return True

    def found__(self, status, index, element_len):
        self.current_state = "id"
        return True

    def id_found(self, status, index, element_len):
        if index >= element_len:
            return True
        return self.crossroad(status, index, element_len)

#def lex_hub(token_record):
    #count = 0
    # for loop for len of list
        # If "undefined":
            #for loop to figure out len of str
                 #if first element .is_alpha()
                    #id_fsm
                 #elif first element .isdigit()
                    ##### We gotta figure out how to handle reals
                    #int_fsm
                 #else:
                    #kill switch to end compiler

            # place back in list
        # else:
            #count +=1
    #return list

def main():
    users_input = user_input()
    token_record = queue_hub(users_input)
    refined_token = operator_smasher(token_record)
    #lex_hub(token_record)
    for token in refined_token:
        print(token)


    #test for id_fsm
    # example = "1337"
    # fsm = id_fsm()
    # result = all(fsm.transition(char, idx, len(example)) for idx, char in enumerate(example))
    # print("Valid Identifier:", result)  


    

if __name__ ==  "__main__":
    main()

