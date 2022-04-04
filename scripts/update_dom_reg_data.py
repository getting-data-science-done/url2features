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
import json
import whois

dict_file = 'url2features/data/dom_reg.dat' 

with open(dict_file, 'r') as file:
    lookup =  json.loads(file)

df = pd.read_csv("../attention-and-context/ranking_analysis/data/URLs.csv")

def extract_domain(url):
    parts = url.split("/")
    if len(parts)>1:
        return parts[0]
    return url

df['domain'] = df['referrer'].apply(extract_domain)

def remove_subdomain(url):
    if url[0:3]=='www':
        return url[4:]
    splitd = url.split(".")
    while len(splitd)>3:
        url = url[len(splitd[0])+1:]
        splitd = url.split(".")
    return url

df['domain2'] = df['domain'].apply(remove_subdomain)

newdf = df.groupby('domain2').agg({'referrer':'count'}).reset_index()

for dom in newdf['domain2']:    
    if dom not in lookup:
        try:
            w2 = whois.whois(dom)
            if isinstance(w2.creation_date, list):
                created = w2.creation_date[0]
            else:
                created = w2.creation_date
            lookup[dom] = created
        except:
            lookup[dom] = "" 

with open(dict_file, 'w') as file:
     file.write(json.dumps(lookup))


