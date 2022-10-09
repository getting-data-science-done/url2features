import time
import pandas as pd
import urllib.request

df = pd.read_csv("dmoz_dataset_head.csv")

all_links = df["URL"].to_list()

response_times = []
active_links = []

for x in all_links:
    st = time.time()
    try:
        rez = urllib.request.urlopen(x).getcode()
        active = 1
    except:
        active = 0
    et = time.time()
    resp = et - st
    response_times.append(resp)
    active_links.append(active)

total_data = pd.DataFrame({"URL":all_links, "active":active_links, "response":response_times})

total_data.to_csv("DMOZ_active_response_test.csv", index=False, header=True)

