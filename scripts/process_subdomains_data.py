# ########################################################################################
# Subdomain Frequency Data Processing
# We copied the table of data available here:
# bitquark_20160227_subdomains_popular_1000_with_count.txt
# Downloaded from
# https://github.com/bitquark/dnspop/blob/master/results/bitquark_20160227_subdomains_popular_1000_with_count
# and then process it into a dictionary of frequencies
#
# ###################################

import pandas as pd
import json

file = "data/bitquark_20160227_subdomains_popular_1000_with_count.txt"
df = pd.read_csv(file, sep=" ", header=None, names=['Count','Subdomain'])

df['freq'] = df['Count']/(df['Count'].sum())

lookup = pd.Series(df.freq.values, index=df.Subdomain).to_dict()

with open('url2features/data/subdomain_freqs.dat', 'w') as file:
     file.write(json.dumps(lookup))

