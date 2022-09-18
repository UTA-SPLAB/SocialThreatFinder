
from stf_main_driver import *

def run(): # Runs Social ThreatFinder

    from pyfiglet import Figlet
    custom_fig = Figlet(font='straight')
    print(custom_fig.renderText('Social ThreatFinder'))

    while 1: 
        
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
