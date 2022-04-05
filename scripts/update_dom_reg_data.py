# ###################################################################################
# Domain Registrations Data Update
#
# Purpose of this script is to update the dictionary of domain regsitration dates
# provide this script a path to a CSV file that contains URLs and it will 
# identify the unique domains, extract the subdomain (best it can) and then
# add an entry if needed by querying WHOIS.
# ###################################
import numpy as np
import pandas as pd
import argparse
import json
import whois
import os
import sys

oldfile = "../attention-and-context/ranking_analysis/data/URLs.csv"

dict_file = 'url2features/data/dom_reg.dat' 

####################################################################
"""
Utility functions used by main()
"""
def extract_domain(url):
    parts = url.split("/")
    if len(parts)>1:
        return parts[0]
    return url

def remove_subdomain(url):
    if url[0:3]=='www':
        return url[4:]
    splitd = url.split(".")
    while len(splitd)>3:
        url = url[len(splitd[0])+1:]
        splitd = url.split(".")
    return url

####################################################################
def main(datafile, urlcol, sep=","):
    """
    Main function for processing the datafile to add all the domains
    to the lookup dictionary
    """ 
    df = pd.read_csv(datafile, sep=sep)

    with open(dict_file, 'r') as file:
        lookup =  json.loads(file.read())

    df['domain'] = df[urlcol].apply(extract_domain)
 
    df['domain2'] = df['domain'].apply(remove_subdomain)

    newdf = df.groupby('domain2').agg({urlcol:'count'}).reset_index()

    for dom in newdf['domain2']:
        dom = dom.lower()   
        if dom not in lookup:
            try:
                w2 = whois.whois(dom)
                if isinstance(w2.creation_date, list):
                    created = w2.creation_date[0]
                else:
                    created = w2.creation_date
                lookup[dom] = str(created)
            except:
                lookup[dom] = "" 

    with open(dict_file, 'w') as file:
         file.write(json.dumps(lookup))

#########################################################################
if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='Update the library domain reg data')
    my_parser.add_argument('data',
                       metavar='data',
                       type=str,
                       help='Path to CSV file containing URLs')
    my_parser.add_argument('col',
                       metavar='col',
                       type=str,
                       help='Name of the column that contains URLs')
 
    my_parser.add_argument('--sep', nargs='?', const=1, type=str, default=",")

    args = my_parser.parse_args()
    data = args.data
    col = args.col
    sep = args.sep

    if not os.path.isfile(data):
        print(" ERROR")
        print(" The input file '%s' does not exist" % data)
        sys.exit()

    main(data, col, sep)


