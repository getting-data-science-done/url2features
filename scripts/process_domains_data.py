# ########################################################################################
# Top Level Domain Frequency Data Processing
# We copied the file https://raw.githubusercontent.com/tb0hdan/domains/master/STATS.md
# and modified it so that it was a tab separted value data file of the TLD counts
#
# ###################################

import pandas as pd
import json

df = pd.read_csv("data/domains.csv", sep="\t", header=None, names=['domain', 'type', 'registar'])

df['domain'] = df['domain'].apply(lambda x : x.replace('.', '') )

lookup = pd.Series(df.type.values, index=df.domain).to_dict()

with open('url2features/data/domains.dat', 'w') as file:
     file.write(json.dumps(lookup))

