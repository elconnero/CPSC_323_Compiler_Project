import os
import sys

def get_base_dir():
    # If running from executable
    if getattr(sys, 'frozen', False):
        # Get the directory where the executable is located
        executable_dir = os.path.dirname(sys.executable)
        # Go up one level from dist/main to get to the root project directory
        return os.path.dirname(os.path.dirname(executable_dir))
    else:
        # Get the directory where the script is located
        return os.path.dirname(os.path.abspath(__file__)) 