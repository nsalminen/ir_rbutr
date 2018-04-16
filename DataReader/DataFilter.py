import pandas as pd
import requests

source = "sourcepage"
rebuttal = "rebuttalpage"
df = pd.read_csv("data.tab", sep="\t", header=0, usecols=[source, rebuttal])

blacklist = [".pdf", "twitter", "youtube", "http://rbutr.com/fauxNews.html", "reddit"]

for s in blacklist:
    df = df[df.sourcepage.str.contains(s) == False]
    df = df[df.rebuttalpage.str.contains(s) == False]

df.to_csv("filtered.tab", sep="\t")

# Possible check for unreachable web pages
# Note that this will take a long time and does only
# idicate the unreachable webpages and does not remove the entries.

# dfc = df
# counter = 0
#
# for idx, row in dfc.iterrows():
#     try:
#         r = requests.head(row.sourcepage)
#         print(row.sourcepage + " " + str(r.status_code))
#         if r.status_code == 302 or r.status_code == 301:
#             r1 = requests.get(row.sourcepage)
#             print(r1.status_code)
#         if r.status_code == 200:
#             counter = counter + 1
#     except:
#         continue
#
#
# print(counter)
