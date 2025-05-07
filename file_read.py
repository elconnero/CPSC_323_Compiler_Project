import os
import sys
from utils import get_base_dir

files = [
    "source_rat25s.txt",     #0
    "newtestcase1.txt",      #1
    "newtestcase2.txt",      #2
    "newtestcase3.txt",      #3        
    "enter manual file name" #4 
    # Make sure that this is the last file, because of the code we have below, this will take an input from the user.
] # Can enter any types of test cases for the final, we should have many different types that the user may enter. 

def user_selection():
    base_dir = get_base_dir()
    
    # Make sure to change this the further we get in homework and what not. 
    print(f"""
          CPSC 323 Compiler Project Assignment 2 Syntax Analyzer\n
          {len(files)-1} files that can be tested. If you would like to use your own file, select int({len(files)}) below.\n
          """)

    # This is here to name all the files and what not. 
    for i in range(len(files)):
        print(f'{i+1}. {files[i]}')

    while True: # Where bulk of user selection happens. 
        try:
            user_input = int(input ("Enter the number next to file name you would like to test.\nEnter here: "))
            if 1 <= user_input <=len(files):
                if user_input <len(files):
                    selected_file = files[user_input-1]
                    # Check if file exists in base directory
                    file_path = os.path.join(base_dir, selected_file)
                    if not os.path.exists(file_path):
                        print(f"Error: {selected_file} not found in {base_dir}. Please ensure the file exists.")
                        continue
                    print(f"\nTROUBLESHOOT\nuser sent to line 27, Userselected {selected_file} int({user_input-1}) to files.") # Make sure to get rid of this once done troubleshooting. REPORT: Working as intented. 
                    return selected_file
                else:
                    custom_file_name = input ("Enter the name of the file you wish to bring into program.\nEnter Here: ")
                    # Check if custom file exists in base directory
                    file_path = os.path.join(base_dir, custom_file_name)
                    if not os.path.exists(file_path):
                        print(f"Error: {custom_file_name} not found in {base_dir}. Please ensure the file exists.")
                        continue
                    return custom_file_name
            else:
                print(f"Please enter a number between 1 and {len(files)}.")
        except ValueError:
            print("Invalid input. Input a valid number.\nEnter here:")

def read_source_file(filename):
    base_dir = get_base_dir()
    file_path = os.path.join(base_dir, filename)
    
    try:
        with open(file_path, "r") as f:
            code = f.read()
        return code
    except FileNotFoundError:
        print(f"Error: {filename} not found in {base_dir}. Please ensure the file exists.")
        sys.exit(1)

def file_read():
    # This is where we are going to create the calls for this .py to main.py
    intake = user_selection()
    source_code = read_source_file(intake)
    return source_code

def syntax_testcase(): # A way to open any file you want without having to jump through hoops. 
    source_code = read_source_file('me1.txt')
    return source_code

def file_output(x, file, tokens):
    
    if x == 1:
        filename = file
    else:
        filename = file
    
    base_dir = get_base_dir()
    lexer_output_filename = os.path.join(
        base_dir,
        os.path.splitext(os.path.basename(filename))[0] + "_lexer_output.txt"
    )

    with open(lexer_output_filename, "w") as out_file:
        out_file.write("Token\t\tLexeme\n")
        for token in tokens:
            out_file.write(f"{token[1]:<10}\t{token[0]}\n")
    
    print(f"Lexer output written to: {lexer_output_filename}")


# Trouble shooting area
def main(): 
    user_selection()                    

if __name__ == "__main__":
    main()

