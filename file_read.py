files = [
    "source_rat25s.txt",     #0
    "testcase1.txt",         #1
    "testcase2.txt",         #2
    "me1.txt",               #3        
    "enter manuel file name" #4 
    # Make sure that this is the last file, because of the code we have below, this will take an input from the user.
] # Can enter any types of test cases for the final, we should have many different types that the user may enter. 

def user_selection():
    
    # Make sure to change this the further we get in homework and what not. 
    print(f"CPSC 323 Compiler Project Assignment 2 Syntax Analyzer\n{len(files)-1} files that can be tested. If you would like to use your own file, select int({len(files)}) below.\n")
     # Make sure to change this the further we get in homework and what not.

    # This is here to name all the files and what not. 
    for i in range(len(files)):
        print(f'{i+1}. {files[i]}')

    while True:
        try:
            user_input = int(input ("Enter the number next to file name you would like to test.\nEnter here: "))
            if 1 <= user_input <=len(files):
                if user_input <len(files):

                    print(f"\nTROUBLESHOOT\nuser sent to line 27, Userselected {files[user_input-1]} int({user_input-1}) to files.") # Make sure to get rid of this once done troubleshooting. REPORT: Working as intented. 
                    return files[user_input-1]
                else:
                    custom_file_name = input ("Ensure file you wish to analyze is in the same folder as main.py, furthermore ensure the filename is as exactly as it is in explorer.\nExample[sample_test_case.txt]\nEnter the name of the file you wish to bring into progam.\nEnter Here: ")
                    return custom_file_name
            else:
                print(f"Please enter a number between 0 and {len(files) - 1}.")
        except ValueError:
            print("Invalid input. Input a valid number.\nEnter here:")

def read_source_file(filename):
    
    try:
        with open(filename, "r") as f:
            code = f.read()
        return code
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please ensure the file exists.")
        exit(1)

def file_read():
    # This is where we are going to create the calls for this .py to main.py
    intake = user_selection()
    source_code = read_source_file(intake)
    return source_code

# Trouble shooting area
def main(): 
    user_selection()                    

if __name__ == "__main__":
    main()