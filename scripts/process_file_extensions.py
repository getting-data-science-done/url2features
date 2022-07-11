# ########################################################################################
# Top Level Domain Frequency Data Processing
# We copied the file https://raw.githubusercontent.com/tb0hdan/domains/master/STATS.md
# and modified it so that it was a tab separted value data file of the TLD counts
#
# ###################################

import pandas as pd
import json

df = pd.read_csv("data/file_extensions.tsv", sep="\t")

df['ext'] = df['ext'].apply(lambda x : x.replace('.', '') )

lookup = pd.Series(df.type.values, index=df.ext).to_dict()

with open('url2features/data/file_extensions.dat', 'w') as file:
     file.write(json.dumps(lookup))

