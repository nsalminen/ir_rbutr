import pandas as pd

data = pd.read_csv("data.tab", sep="\t", header=0)

count = data.sourcepage.value_counts()

sourceList = []
rebuttalList = []

for idx, row in enumerate(count):
    if 23 < row < 30:
        source = (count.index[idx])
        sourceList.append(source)
        print(data[data["sourcepage"].str.contains(source)].rebuttalpage)
        rebuttalList.append(data[data["sourcepage"].str.contains(source)].rebuttalpage)


print(sourceList)
print(rebuttalList[0])

file = open("output.txt", 'w')
file.write(str(sourceList))



# count = data.groupby("sourcepage").linkid.nunique()
#
# print(count.dtype)
#
# print(count)
#
# for item in count:
#     if(item > 10):
#         print(item)

# for index,row in count.iterrows():
#     print(row["sourcepage"])

# for index,row in data.iterrows():
#     print(row["linkid"])