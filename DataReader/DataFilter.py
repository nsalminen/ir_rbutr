import pandas as pd
import requests

source = "sourcepage"
rebuttal = "rebuttalpage"
df = pd.read_csv("data.tab", sep="\t", header=0, usecols=[source, rebuttal])

pdf = ".pdf"
twitter = "twitter"
youtube = "youtube"
rbutr = "http://rbutr.com/fauxNews.html"
reddit = "reddit"

df = df[df.sourcepage.str.contains(youtube) == False]
df = df[df.sourcepage.str.contains(twitter) == False]
df = df[df.sourcepage.str.contains(pdf) == False]
df = df[df.sourcepage.str.contains(reddit) == False]
df = df[df.sourcepage.str.contains(rbutr) == False]

df = df[df.rebuttalpage.str.contains(youtube) == False]
df = df[df.rebuttalpage.str.contains(twitter) == False]
df = df[df.rebuttalpage.str.contains(pdf) == False]
df = df[df.rebuttalpage.str.contains(reddit) == False]
df = df[df.rebuttalpage.str.contains(rbutr) == False]

df.to_csv("out.tab", sep="\t")

# Possible check for unreachable web pages

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
