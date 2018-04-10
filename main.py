import nltk
import time
import sys
from urllib.request import Request, urlopen
from ModLexRank import ModLexRank
from lexrank import STOPWORDS
from newspaper import Article, Config
from SourceArticle import SourceArticle
from tqdm import tqdm, trange

def readDataFile(path, sourceArticleList):
	with open(path) as f:
		content = [x.strip('\n') for x in f] 

	idx = 0
	pbar = tqdm(total=len(content), unit="line", desc="Reading " + path)
	while idx < len(content):
		if (content[idx] == 'new node'):
			idx = idx + 1
			sourceArticleList.append(SourceArticle(content[idx]))
			pbar.update(1)
		elif (content[idx] != 'list'):
			sourceArticleList[-1].rebutalUrlList.append(content[idx])
		pbar.update(1)
		idx = idx + 1

sourceArticleList = list()
readDataFile("output.txt", sourceArticleList)
pbar = tqdm(total=len(sourceArticleList), unit="article", desc=("Summarizing " + str(len(sourceArticleList)) + " articles"))
for idx, val in enumerate(sourceArticleList):
	summary = sourceArticleList[idx].summarizeRebutals(size=10, summary_threshold = 0.3)
	with open('summary' + str(idx) + '.txt', mode='wt', encoding='utf-8') as summaryFile:
		summaryFile.write(' '.join(summary))
	pbar.update(1)