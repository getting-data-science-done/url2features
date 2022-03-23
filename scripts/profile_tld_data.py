# ########################################################################################
# Top Level Domain Frequency Data Processing
# We copied the file https://raw.githubusercontent.com/tb0hdan/domains/master/STATS.md
# and modified it so that it was a tab separted value data file of the TLD counts
#
# ###################################

import pandas as pd
import json

df = pd.read_csv("data/tld.tsv", sep="\t")

total = df['count'].sum()

df['freq'] = 100 * df['count']/total

lookup = pd.Series(df.freq.values, index=df['tld']).to_dict()

with open('url2features/data/tld.dat', 'w') as file:
     file.write(json.dumps(lookup))

