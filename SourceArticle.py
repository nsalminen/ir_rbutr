from ModLexRank import ModLexRank
from lexrank import STOPWORDS
from newspaper import Article, Config
from tqdm import tqdm, trange
import io

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
	except:
		return ''
	return articleText

class SourceArticle(object):
	"""docstring for SourceArticle""" 
	def __init__(self, sourceUrl):
		super(SourceArticle, self).__init__()
		self.sourceUrl = sourceUrl
		self.rebutalUrlList = list()
		self.rebutalTextList = list()

	def __repr__(self):
		return "<Source URL:%s Rebutal count:%s>" % (self.sourceUrl, len(self.rebutalUrlList))

	def summarizeRebutals(self, size, summary_threshold=0.1):
		unsuccessfulRetrievals = list()
		for url in tqdm(self.rebutalUrlList, unit="rebutal", desc="Retrieving and parsing data from URLs"):
			urlText = retrieveUrlText(url)
			if urlText != '':
				self.rebutalTextList.append(urlText)
			else:
				unsuccessfulRetrievals.append(url)
		if unsuccessfulRetrievals:
			print('\033[1m'+"URL retrieval failed for URLs: " + '\033[0m' + ', '.join(unsuccessfulRetrievals) + '\r')
		self.rebutalTextList = [self.rebutalTextList]
		lxr = ModLexRank(self.rebutalTextList, stopwords=STOPWORDS['en'])
		summary = lxr.get_summary(summary_size=size, threshold=summary_threshold)
		return summary