from ModLexRank import ModLexRank
from lexrank import STOPWORDS
from newspaper import Article, Config
from tqdm import tqdm
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from urlextract import URLExtract
import re


def validateSentences(sentences):
        newSentenceList = list()
        for s in sentences:
            bracketContent = re.findall(r'\[(.*?)\]', s)
            bracketDiscount = 0
            if bracketContent:
                bracketDiscount = len(''.join(bracketContent))
                s = re.sub(r'\s?\[([0-9]+)\]\s?', '', s)
            alphaCount = sum(c.isalpha() for c in s) - bracketDiscount
            if (alphaCount < 15 or alphaCount > 130 or len(s.split()) < 4):
                continue
            extractor = URLExtract()
            urls = extractor.find_urls(s)
            if (urls):
                continue
            newSentenceList.append(s)
        return newSentenceList


def retrieveUrlText(url):
    try:
        config = Config()
        config.request_timeout = 1000
        config.memoize_articles = False
        config.fetch_images = False
        config.browser_user_agent = 'Mozilla/5.0'
        article = Article(url, config)
        article.download(recursion_counter=5)
        if article.download_state != 2:
            return ''
        article.parse()
        articleText = article.text.replace('\n', ' ')
    except KeyboardInterrupt:
        raise
    except Exception:
        return ''
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'et', 'al', 'fig', 'figs', 'chem', 'ph'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    articleSentences = validateSentences(sentence_splitter.tokenize(articleText))
    return articleSentences


class SourceArticle(object):
    """docstring for SourceArticle"""
    def __init__(self, sourceUrl):
        super(SourceArticle, self).__init__()
        self.sourceUrl = sourceUrl
        self.rebuttalUrlList = list()
        self.rebuttalTextList = list()

    def __repr__(self):
        return "<Source URL:%s Rebuttal count:%s>" % (self.sourceUrl, len(self.rebuttalUrlList))

    def downloadRebuttals(self):
        unsuccessfulRetrievals = list()
        for url in tqdm(self.rebuttalUrlList, unit="rebuttal", desc="Retrieving and parsing data from URLs"):
            urlText = retrieveUrlText(url)
            if urlText != '':
                self.rebuttalTextList.append(urlText)
            else:
                unsuccessfulRetrievals.append(url)
        if unsuccessfulRetrievals:
            print('\033[1m' + "URL retrieval failed for URLs: " + '\033[0m' + ', '.join(unsuccessfulRetrievals) + '\r')

    def summarizeRebuttals(self, size, summary_threshold=0.1):
        lxr = ModLexRank(self.rebuttalTextList, stopwords=STOPWORDS['en'])
        summary = lxr.get_summary(summary_size=size, threshold=summary_threshold)
        return summary
