#! /usr/bin/python

__author__ = "ping.zou"
__date__ = "$March 16, 2013"

from count_freqs import Hmm
from collections import defaultdict

"""
extend Hmm provided by assigments
"""

RARE_WORD_THRESHOLD = 5


class Hmm_ex(Hmm):
    """
    Store counts, and model params
    """
    def __init__(self, n=3):
        super(Hmm_ex, self).__init__(n)

        self.emission_params = defaultdict(float)  # e(x|y)
        self.word_counts = defaultdict(int)  # count(x)
        self.rare_words = []
        self.tags = set()
        self.words = set()
        self.q_3_gram = defaultdict(float)
        self.rare_word_threshold = RARE_WORD_THRESHOLD

    def train(self, corpus_file):
        """
        Count n-gram frequencies and emission probabilities from a corpus file.
        """
        super(Hmm_ex, self).train(corpus_file)
        self.count_words()  # count(x)
        self.get_rare_words(self.rare_word_threshold)  # rare word
        self.cal_emission_param()  # e(x|y)
        self.get_all_tags_and_words()  # get all tags and words
        self.cal_q_3_gram()  # q(y_i|y_i-2, y_i_1)

    def get_all_tags_and_words(self):
        for word, tag in self.emission_counts:
            self.tags.add(tag)
            self.words.add(word)

    def count_words(self):
        '''
        count(x)
        '''
        for word, tag in self.emission_counts:
            self.word_counts[word] += self.emission_counts[(word, tag)]

    def get_rare_words(self, threshold):
        self.rare_words = []
        for word in self.word_counts:
            if self.word_counts[word] < threshold:
                self.rare_words.append(word)

    def cal_emission_param(self):
        """
        e(x|y) = count(y->x) / count(y)
               = emission_counts[(y, x)] / ngram_counts[0][y]
        """
        for k in self.emission_counts.keys():
            # print k, self.emission_counts[k], tuple(k[-1:]), self.ngram_counts[0][tuple(k[-1:])]
            self.emission_params[k] = float(self.emission_counts[k]) / float(self.ngram_counts[0][tuple(k[-1:])])
            # print self.emission_params[k]

    def cal_q_3_gram(self):
        """
        q(y_i|y_i-2, y_i_1) = count(y_i-2, y_i-1, y_i) / count(y_i-2, y_i-1)
        """
        for c in self.ngram_counts[2]:
            self.q_3_gram[c] = float(self.ngram_counts[2][c]) / float(self.ngram_counts[1][tuple(c[0:2])])

    def read_counts(self, corpusfile):
        super(Hmm_ex, self).read_counts(corpusfile)

        self.word_counts = defaultdict(int)
        self.emission_params = defaultdict(float)
        self.rare_words = []
        self.q_3_gram = defaultdict(float)

        self.cal_emission_param()
        self.count_words()
        self.get_rare_words(self.rare_word_threshold)
        self.get_all_tags_and_words()
        self.cal_q_3_gram()

    def print_emission_counts(self, output):
        for word, ne_tag in self.emission_counts:
            output.write("%i WORDTAG %s %s\n" % (self.emission_counts[(word, ne_tag)], ne_tag, word))

    def print_ngram_counts(self, output, printngrams=[1, 2, 3]):
        for n in printngrams:
            for ngram in self.ngram_counts[n-1]:
                ngramstr = " ".join(ngram)
                output.write("%i %i-GRAM %s\n" % (self.ngram_counts[n-1][ngram], n, ngramstr))

    def print_emission_params(self, output):
        for word, ne_tag in self.emission_params:
            output.write('{0} EMISSION_PARAM {1} {2}\n'.format(self.emission_params[(word, ne_tag)], ne_tag, word))

    def print_word_counts(self, output):
        for word in self.word_counts:
            output.write('{0} WORDCOUNT {1}\n'.format(self.word_counts[word], word))

    def print_rare_words(self, output):
        for word in self.rare_words:
            output.write('{0} RAREWORD {1}\n'.format(self.word_counts[word], word))

    def print_q_3_gram(self, output):
        for ngram in self.q_3_gram:
            output.write('{0} Q_3_GRAM {1} {2} {3}\n'.format(
                self.q_3_gram[ngram],
                ngram[0],
                ngram[1],
                ngram[2]))
