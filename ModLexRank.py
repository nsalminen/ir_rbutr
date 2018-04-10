from lexrank import STOPWORDS, LexRank
import math
from collections import Counter, defaultdict
import nltk
import re
from urlextract import URLExtract
import numpy as np

from lexrank.algorithms.power_method import stationary_distribution
from lexrank.utils.text import tokenize

class ModLexRank(LexRank):
	"""docstring for ModLexRank"""
	def validateSentence(self, s):
		alphaCount = sum(c.isalpha() for c in s)
		if (alphaCount < 15 or alphaCount > 130):
			return False
		extractor = URLExtract()
		urls = extractor.find_urls(s)
		if (urls):
			return False
		return True

	def __init__(
		self,
		documents,
		stopwords=None,
		keep_numbers=False,
		keep_emails=False,
		include_new_words=True,
	):
		if stopwords is None:
			self.stopwords = set()
		else:
			self.stopwords = stopwords

		self.doc_sentences = list()
		self.keep_numbers = keep_numbers
		self.keep_emails = keep_emails
		self.keep_urls = False
		self.include_new_words = include_new_words

		bags_of_words = []

		for doc in documents:
			doc_words = set()

			for sentence in doc:
				articleSentences = nltk.sent_tokenize(sentence)
				articleSentences[:] = [tup for tup in articleSentences if self.validateSentence(s=tup)]
				self.doc_sentences = self.doc_sentences + articleSentences
				words = self.tokenize_sentence(sentence)
				doc_words.update(words)

			if doc_words:
				bags_of_words.append(doc_words)

		if not bags_of_words:
			raise ValueError('documents are not informative')
		self.bags_of_words = bags_of_words
		self.idf_score = self._calculate_idf()

	def get_summary(
		self,
		summary_size=1,
		threshold=.03,
		discretize=True,
		fast_power_method=True,
	):
		if not isinstance(summary_size, int) or summary_size < 1:
			raise ValueError('\'summary_size\' should be a positive integer')

		lexrank = self.rank_sentences(
			self.doc_sentences,
			threshold=threshold,
			discretize=discretize,
			fast_power_method=fast_power_method,
		)

		sorted_ix = np.argsort(lexrank)[::-1]
		summary = [self.doc_sentences[i] for i in sorted_ix[:summary_size]]

		return summary