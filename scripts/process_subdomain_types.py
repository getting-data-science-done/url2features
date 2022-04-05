# ########################################################################################
# Subdomain Type Data Processing
# ###################################
import numpy as np
import pandas as pd
import json

file = "data/subdomains.tsv"
df = pd.read_csv(file, sep="\t")

webType = ['www','ww1','www1','ww2','www2','ww42','web','m','mobile']
conType = ['finance', 'sport', 'style', 'news', 'lifestyle', 'food', 'arts', 'film','video','tv','books','tech','science','fashion','beauty','celeb','celebrity','gossip','travel','health','home','garden'] 
specType = ['blog','community','forum','shop','store','support','docs','media','wiki','login','admin','portal']
mailType = ['mail','email','mail1','mail2','webmail','smtp','exchange','owa','mx','mx0','mx1','mx2','mxb','aspmx','mailserver','pop','pop3','mailin1','mailin2','inbound','imap','office']
utilType = ['ftp','remote','vpn','bbs','2tty']
infraType = ['dns','dns1','dns2','ns1','ns2','ns3','ns4','ns5','ns6','ns7','ns8','ns','server','host','cloud','cdn','test','dev','api','ssl','vps']

df['type'] = np.where(
    df['Subdomain'].isin(conType), 7,
    np.where(
        df['Subdomain'].isin(specType), 6, 
        np.where(
            df['Subdomain'].isin(webType), 5,
            np.where(
                df['Subdomain'].isin(mailType), 4,
                np.where(
                    df['Subdomain'].isin(utilType), 3, 
                    np.where(
                        df['Subdomain'].isin(infraType), 2, 1
                    )
                )
            )
        )
    )
)

lookup = pd.Series(df.type.values, index=df.Subdomain).to_dict()

with open('url2features/data/subdomain_types.dat', 'w') as file:
     file.write(json.dumps(lookup))

