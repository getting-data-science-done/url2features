# ########################################################################################
# Domain Registrations Data Processing
#
# ###################################
import numpy as np
import pandas as pd
import json
import whois

dict_file = 'url2features/data/dom_reg.dat'

with open(dict_file, 'r') as file:
    lookup =  json.loads(file.read())

initlist = ['google.com', 'facebook.com', 'linkedin.com', 'twitter.com',
    'youtube.com','wikipedia.org', 'amazon.com', 'instagram.com', 'yahoo.com', 
    'yandex.ru', 'pornhub.com','reddit.com','naver.com','xvideos.com','bit.ly',
    'vk.com','live.com','xnxx.com','fandom.com','yahoo.co.jp','twitch.tv'
]

for dom in initlist:
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
    else:
        print(dom, " already processed")

with open(dict_file, 'w') as file:
     file.write(json.dumps(lookup))


