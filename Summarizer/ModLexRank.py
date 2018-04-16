from lexrank import STOPWORDS, LexRank
from lexrank.algorithms.power_method import stationary_distribution
from lexrank.utils.text import tokenize

import numpy as np
from tqdm import tqdm
import math


class ModLexRank(LexRank):
    """docstring for ModLexRank"""
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
                self.doc_sentences.append(sentence)
                words = self.tokenize_sentence(sentence)
                doc_words.update(words)

            if doc_words:
                bags_of_words.append(doc_words)

        if not bags_of_words:
            raise ValueError('documents are not informative')
        self.bags_of_words = bags_of_words
        self.idf_score = self._calculate_idf()

    def _markov_matrix_discrete(self, similarity_matrix, threshold):
        markov_matrix = np.zeros(similarity_matrix.shape)
        for i in range(len(similarity_matrix)):
            columns = np.where(similarity_matrix[i] > threshold)[0]
            markov_matrix[i, columns] = 1 / len(columns)

        return markov_matrix

    def rank_sentences(
        self,
        sentences,
        threshold=.03,
        discretize=True,
        fast_power_method=True,
        normalize=False,
    ):
        if not isinstance(threshold, float) or not 0 <= threshold < 1:
            raise ValueError(
                '\'threshold\' should be a floating-point number '
                'from the interval [0, 1)',
            )

        tf_scores = [
            self._calculate_tf(self.tokenize_sentence(sentence))
            for sentence in sentences
        ]
        similarity_matrix = self._calculate_similarity_matrix(tf_scores)
        np.savetxt('text.txt', similarity_matrix, delimiter=' ', fmt='%.2f')
        if discretize:
            markov_matrix = self._markov_matrix_discrete(
                similarity_matrix,
                threshold=threshold,
            )

        else:
            markov_matrix = self._markov_matrix(similarity_matrix)

        lexrank = stationary_distribution(
            markov_matrix,
            increase_power=fast_power_method,
        )

        if normalize:
            max_val = max(lexrank)
            lexrank = [val / max_val for val in lexrank]

        return lexrank

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
            sentences=self.doc_sentences,
            threshold=threshold,
            discretize=discretize,
            fast_power_method=fast_power_method,
        )
        sorted_ix = np.argsort(lexrank)[::-1]
        relative_summary_size = math.ceil(len(sorted_ix) * 0.05)
        summary = [self.doc_sentences[i] for i in sorted_ix[:relative_summary_size]]

        return summary
