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

# documents = []
# documents_dir = Path('bbc/politics')

# for file_path in documents_dir.files('*.txt'):
#     with file_path.open(mode='rt', encoding='utf-8') as fp:
#         documents.append(fp.readlines())
# print(documents)
# lxr = ModLexRank(documents, stopwords=STOPWORDS['en'])

# sentences = [
#     'One of David Cameron\'s closest friends and Conservative allies, '
#     'George Osborne rose rapidly after becoming MP for Tatton in 2001.',

#     'Michael Howard promoted him from shadow chief secretary to the '
#     'Treasury to shadow chancellor in May 2005, at the age of 34.',

#     'Mr Osborne took a key role in the election campaign and has been at '
#     'the forefront of the debate on how to deal with the recession and '
#     'the UK\'s spending deficit.',

#     'Even before Mr Cameron became leader the two were being likened to '
#     'Labour\'s Blair/Brown duo. The two have emulated them by becoming '
#     'prime minister and chancellor, but will want to avoid the spats.',

#     'Before entering Parliament, he was a special adviser in the '
#     'agriculture department when the Tories were in government and later '
#     'served as political secretary to William Hague.',

#     'The BBC understands that as chancellor, Mr Osborne, along with the '
#     'Treasury will retain responsibility for overseeing banks and '
#     'financial regulation.',

#     'Mr Osborne said the coalition government was planning to change the '
#     'tax system \"to make it fairer for people on low and middle '
#     'incomes\", and undertake \"long-term structural reform\" of the '
#     'banking sector, education and the welfare state.',
# ]

# # get summary with classical LexRank algorithm
# summary = lxr.get_summary(sentences, summary_size=2, threshold=.1)
# print(summary)