# ########################################################################################
# Subdomain Type Data Processing
# ###################################
import numpy as np
import pandas as pd
import json

file = "data/subdomains.tsv"
df = pd.read_csv(file, sep="\t")

webType = ['www','ww1','www1','ww2','www2','ww42','web','m','mobile']
specType = ['blog','news','forum','shop','store','support','docs','media','wiki','login','admin','portal']
mailType = ['mail','email','mail1','mail2','webmail','smtp','exchange','owa','mx','mx1','mx2','office']
utilType = ['ftp','remote','vpn','bbs','2tty']
infraType = ['ns1','ns2','ns','server','host','cloud','cdn','test','dev','api','ssl','vps']

df['type'] = np.where(
    df['Subdomain'].isin(webType), 6, 
    np.where(
        df['Subdomain'].isin(specType), 5,
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

lookup = pd.Series(df.type.values, index=df.Subdomain).to_dict()

with open('url2features/data/subdomain_types.dat', 'w') as file:
     file.write(json.dumps(lookup))

