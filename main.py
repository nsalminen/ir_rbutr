import nltk
import time
from urllib.request import Request, urlopen
from ModLexRank import ModLexRank
from lexrank import STOPWORDS
from newspaper import Article, Config
from SourceArticle import SourceArticle

def readDataFile(path, sourceArticleList):
	with open(path) as f:
		content = [x.strip('\n') for x in f] 
	
	idx = 0
	while idx < len(content):
		if (content[idx] == 'new node'):
			idx = idx + 1
			sourceArticleList.append(SourceArticle(content[idx]))
		elif (content[idx] != 'list'):
			sourceArticleList[-1].rebutalUrlList.append(content[idx])
		idx = idx + 1

sourceArticleList = list()
readDataFile("output.txt", sourceArticleList)
for idx, val in enumerate(sourceArticleList):
	summary = sourceArticleList[idx].summarizeRebutals(size=10)
	print(summary)
	with open('summary' + str(idx) + '.txt', mode='wt', encoding='utf-8') as summaryFile:
		summaryFile.write(' '.join(summary))