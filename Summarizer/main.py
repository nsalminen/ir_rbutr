from SourceArticle import SourceArticle
from tqdm import tqdm
from lexrank import STOPWORDS, LexRank
from path import Path
from ModLexRank import ModLexRank


def readDataFile(path, sourceArticleList):
    with open(path) as f:
        content = [x.strip('\n') for x in f]

    idx = 0
    pbar = tqdm(total=len(content), unit=" lines", desc="Reading " + path)
    while idx < len(content):
        if (content[idx] == 'new node'):
            idx = idx + 1
            sourceArticleList.append(SourceArticle(content[idx]))
            pbar.update(1)
        elif (content[idx] != 'list'):
            sourceArticleList[-1].rebuttalUrlList.append(content[idx])
        pbar.update(1)
        idx = idx + 1


sourceArticleList = list()
readDataFile("output.txt", sourceArticleList)
pbar = tqdm(total=len(sourceArticleList), unit="article",
            desc=("Summarizing " + str(len(sourceArticleList)) + " articles"))
threshold = 0.5
for idx, val in enumerate(sourceArticleList):
    sourceArticleList[idx].downloadRebuttals()
    summary = sourceArticleList[idx].summarizeRebuttals(size=10, summary_threshold=threshold)
    with open('summary' + str(idx) + '_t' + str(threshold) + '.txt', mode='wt', encoding='utf-8') \
            as summaryFile:
                summaryFile.write(' '.join(summary))
    pbar.update(1)
    pbar.close()
