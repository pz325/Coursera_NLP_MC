#! /usr/bin/python

__author__ = "ping.zou"
__date__ = "$March 16, 2013"

from count_freqs import Hmm
from collections import defaultdict
import util
from decimal import Decimal

"""
extend Hmm provided by assigments
"""


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
        self.rare_word_threshold = util.RARE_WORD_THRESHOLD
        self.rare_words_rule = util.rare_words_rule_p1

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


class SimpleTagger(Hmm_ex):
    """docstring for SimpleTagger"""
    def __init__(self, n=3):
        super(SimpleTagger, self).__init__(n)

    def tag(self, test_data_filename, result_filename):
        # prepare output
        output = file(result_filename, 'w')
        # calcuate arg max e('_RARE_'|y)
        max_e_rare_y, max_rare_y = -1.0, ''
        for tag in self.tags:
            e = self.emission_params[(util.RARE_TAG, tag)]
            if e > max_e_rare_y:
                max_e_rare_y, max_rare_y = e, tag
        # load test_data
        word_iterator = util.test_data_iterator(file(test_data_filename))
        # tag
        for word in word_iterator:
            max_e, max_y = -1.0, ''
            if word is not None:
                if word == util.RARE_TAG or word not in self.words:
                    max_y = max_rare_y
                else:
                    for tag in self.tags:
                        e = self.emission_params[(word, tag)]
                        if e > max_e:
                            max_e, max_y = e, tag
                output.write('{0} {1}\n'.format(word, max_y))
            else:
                output.write('\n')


class ViterbiTagger(Hmm_ex):
    """docstring for ViterbiTagger"""
    def __init__(self, n=3):
        super(ViterbiTagger, self).__init__(n)

    def tag(self, test_data_file, result_file):
        # get test sentence
        sent_iterator = util.test_sent_iterator(
            util.test_data_iterator(test_data_file))
        for sent in sent_iterator:
            tags = self.viterbi(sent)
            for s, t in zip(sent, tags):
                result_file.write('{0} {1}\n'.format(s, t))
            result_file.write('\n')

    def viterbi(self, sent):
        """
        tag a sentence using Viterbi algorithm
        apply only 3-gram
        return tag sequence
        """
        n = len(sent)
        pi = []
        bp = []
        for k in range(0, n + 1):
            pi.append(defaultdict(float))
            bp.append(defaultdict(str))
        pi[0][('*', '*')] = 1.0
        # decode
        for k in range(1, n + 1):
            W = self.tags
            U = self.tags
            V = self.tags
            x = sent[k - 1]
            if x in self.rare_words or x not in self.words:
                x = self.rare_words_rule(x)
            if k == 1:
                W = U = ('*',)
            if k == 2:
                W = ('*',)
            for u in U:
                for v in V:
                    if util.DEBUG:
                        print 'k = {0}, u = {1}, v = {2}'.format(k, u, v)
                    max_pi, max_w = -1.0, ''
                    for w in W:
                        if util.DEBUG:
                            print 'calculating Pi[{km1}, {w}, {u}] * q({v}|{w}, {u}) * e({x}|{v})'.format(km1=k-1, u=u, v=v, w=w, x=x)
                            print 'Pi[{km1}, {w}, {u}] = {p}'.format(km1=k-1, w=w, u=u, p=Decimal(pi[k - 1][(w, u)]))
                            print 'q({v}|{w}, {u}) = {p}'.format(v=v, w=w, u=u, p=Decimal(self.q_3_gram[(w, u, v)]))
                            print 'e({x}|{v}) = {p}'.format(x=x, v=v, p=Decimal(self.emission_params[(x, v)]))
                        if self.emission_params[(x, v)] == 0.0:
                            continue
                        tmp = Decimal(pi[k - 1][(w, u)])  \
                            * Decimal(self.q_3_gram[(w, u, v)]) \
                            * Decimal(self.emission_params[(x, v)])
                        if tmp > max_pi:
                            max_pi, max_w = tmp, w
                    if util.DEBUG:
                        print 'Pi[{k}, {u}, {v}] = {max}'.format(k=k, u=u, v=v, max=max_pi)
                        print 'bp[{k}, {u}, {v}] = {bp}'.format(k=k, u=u, v=v, bp=max_w)
                        print '\n'
                    pi[k][(u, v)] = max_pi
                    bp[k][(u, v)] = max_w
            if util.DEBUG:
                print '========================================='
        # trace back
        U = self.tags
        V = self.tags
        max_pi, max_u, max_v = -1.0, '', ''
        for u in U:
            for v in V:
                tmp = Decimal(pi[n][(u, v)]) \
                    * Decimal(self.q_3_gram[(u, v, 'STOP')])
                if tmp > max_pi:
                    max_pi, max_u, max_v = tmp, u, v
        result = range(0, n+1)
        result[n-1], result[n] = max_u, max_v
        for k in range(n-2, 0, -1):
            result[k] = bp[k+2][(result[k+1], result[k+2])]
        return result[1:]
