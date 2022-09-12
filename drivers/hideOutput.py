
# Module to hide stdout from console 

# Credits: @Brigand : https://stackoverflow.com/users/1074592/brigand

import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

