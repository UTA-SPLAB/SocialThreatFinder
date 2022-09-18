
from stf_main_driver import *
import sys
def run(): # Runs Social ThreatFinder

    from pyfiglet import Figlet
    from termcolor import colored

    custom_fig = Figlet(font='big')
    print(custom_fig.renderText('Social ThreatFinder'))
    print(colored("Version 0.19 stable, 09/18/2022", 'blue'))
    print("\n")


    while 1: 
        try:
            if sys.argv[1]=='lite':
                print("Running Social ThreatFinder in Lite Mode.") 
                print(colored("WARNING: Please consider using the Default (Academic Key mode) for getting the most recent reports.", 'red'))

        except:
            print("Running Social ThreatFinder in Default Mode.") 

        print("Refreshing feed")
        blockPrint() # Hide console output 
        remove_files() # Remove hxxps and hxxp metadata from raw_output to prevent clutter
        run_iteration() # Handles all sub drivers to collect and process the reports
        database_sorter() # Sorts database in ascending order
        #populate_from_database() # Generate Social ThreatFinder front-end map. Removed from open-source release 0.19 onwards
        #htg() # Generate database layout for front-end. Removed from open-source release 0.19 onwards
        enablePrint() #View console output to show countdown
        countdown(600) # Wait for 10 mins before starting next iteration
            

run()
