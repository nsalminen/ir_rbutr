from ModLexRank import ModLexRank
from lexrank import STOPWORDS
from newspaper import Article, Config

def retrieveUrlText(url):
	try:
		config = Config()
		config.request_timeout = 1000
		config.memoize_articles = False
		config.fetch_images = False
		config.browser_user_agent = 'Mozilla/5.0'
		article = Article(url, config)
		article.download(recursion_counter=5)
		article.parse()
		articleText = article.text
	except KeyboardInterrupt:
		raise
	except:
		print("Not able to download article.")
		return ''
	#print("Successfully downloaded " + url)
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
		for url in self.rebutalUrlList:
			urlText = retrieveUrlText(url)
			if urlText != '':
				self.rebutalTextList.append(urlText)
		self.rebutalTextList = [self.rebutalTextList]
		lxr = ModLexRank(self.rebutalTextList, stopwords=STOPWORDS['en'])
		summary = lxr.get_summary(summary_size=size, threshold=summary_threshold)
		return summary