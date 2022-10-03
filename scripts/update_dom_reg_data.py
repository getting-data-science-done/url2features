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
import re

dict_file = 'url2features/data/dom_reg.dat' 

common_suffixes = [ '.com', '.net', '.ne.jp', '.de', '.org', '.edu', '.nl', '.info', '.biz', '.co.uk', '.cz', '.dk',
                    '.com.cn', '.mil', '.ac.uk', '.ch', '.eu', '.com.br', '.co.za', '.ad.jp', '.ac.cn', '.com.au',
                    '.or.jp', '.net.au', '.asia', '.ac.jp', '.mobi', '.co.jp', '.sk', '.edu.tw', 'edu.au', '.net.pl', '.gov' ]

####################################################################
"""
Utility functions used by main()
"""
def extract_domain(url):
    url = str(url)
    url = url.strip()
    prot = re.findall("^[a-zA-Z][a-zA-Z]*://", url)
    if len(prot)>0:
        url = url[len(prot[0]):]
    parts = url.split("/")
    domain = parts[0]
    return domain


def remove_subdomain(url):
    url = str(url)
    if url[0:4]=='www.':
        return url[4:]
    if url[0:5]=='www1.':
        return url[5:]
    for sfx in common_suffixes:
       sfl = len(sfx)
       if url[-sfl:] == sfx:
           base = url[0:len(url)-sfl]
           dom = base.split(".")
           if len(dom)>1:
               return dom[-1] + sfx
           else:
              return url
    # IF all that fails trim to a 2 part domain
    splitd = url.split(".")
    while len(splitd)>2:
        url = url[len(splitd[0])+1:]
        splitd = url.split(".")
    return url


def remove_port(url):
    url = str(url)
    return re.sub(':[0-9]*', '', url)

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
    df['domain2'] = df['domain'].apply(remove_port)
    df['domain3'] = df['domain2'].apply(remove_subdomain)

    newdf = df.groupby('domain3').agg({urlcol:'count'}).reset_index()

    for dom in newdf['domain3']:
        print("Processing", dom)
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


