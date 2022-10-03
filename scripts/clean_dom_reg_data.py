# ###################################################################################
# Domain Registrations Data Clean 
#
# Purpose of this script is to clean the dictionary of domain regsitration dates
# ###################################
import numpy as np
import pandas as pd
import json
import os
import sys

dict_file = 'url2features/data/dom_reg.dat' 

####################################################################
def main():
    """
    Main function for processing the datafile to add all the domains
    to the lookup dictionary
    """ 

    with open(dict_file, 'r') as file:
        lookup =  json.loads(file.read())

    delete_list = []
    mydoms = lookup.keys()
    for dom in mydoms:
        if lookup[dom] == "None":
            print("No entry for ", dom)
            delete_list.append(dom)

    for dom in delete_list:
        del lookup[dom]

    with open(dict_file, 'w') as file:
        file.write(json.dumps(lookup))

#########################################################################
if __name__ == '__main__':

    main()

