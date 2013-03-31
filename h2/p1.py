#! /usr/bin/python
import json
from count_cfg_freq import Counts
from collections import defaultdict

__author__ = 'ping.zou'
__date__ = '30 Mar 2013'


RARE_TAG = '_RARE_'
RARE_WORD_THRESHOLD = 5


def rare_words_rule_p1(word):
    return RARE_TAG


def process_rare_words(input_file, output_file, rare_words, processer):
    for line in input_file:
        tree = json.loads(line)
        replace(tree, rare_words, processer)
        output = json.dumps(tree)
        output_file.write(output)
        output_file.write('\n')


def replace(tree, rare_words, processer):
    if isinstance(tree, basestring):
        return

    if len(tree) == 3:
        # Recursively count the children.
        replace(tree[1], rare_words, processer)
        replace(tree[2], rare_words, processer)
    elif len(tree) == 2:
        if tree[1] in rare_words:
            tree[1] = processer(tree[1])


class PCFG(Counts):
    """
    Store counts, and model params
    """
    def __init__(self):
        super(PCFG, self).__init__()

        self.word = defaultdict(int)
        self.rare_words = []
        self.q_x_y1y2 = defaultdict(float)
        self.q_x_w = defaultdict(float)

    def count_word(self):
        '''
        count emitted words and find rare words
        '''
        # count emitted word
        for (sym, word), count in self.unary.iteritems():
            self.word[word] += count
        # find rare word
        for word, count in self.word.iteritems():
            if count < RARE_WORD_THRESHOLD:
                self.rare_words.append(word)


    def cal_rule_params(self):
        # q(X->Y1Y2) = Count(X->Y1Y2) / Count(X)
        for (x, y1, y2), count in self.binary.iteritems():
            key = (x, y1, y2)
            self.q_x_y1y2[key] = float(count) / float(self.nonterm[x])
        # q(X->w) = Count(X->w) / Count(X)
        for (x, w), count in self.unary.iteritems():
            key = (x, w)
            self.q_x_w[key] = float(count) / float(self.nonterm[x])

    def write(self, output):
        for sym, count in self.nonterm.iteritems():
            output.write('{count} NONTERMINAL {sym}\n'.format(count=count, sym=sym))

        for (sym, word), count in self.unary.iteritems():
            output.write('{count} UNARYRULE {sym} {word}\n'.format(count=count, sym=sym, word=word))

        for (sym, y1, y2), count in self.binary.iteritems():
            output.write('{count} BINARYRULE {sym} {y1} {y2}\n'.format(count=count, sym=sym, y1=y1, y2=y2))

    def read(self, input):
        '''
        Read model
        '''
        self.unary = {}
        self.binary = {}
        self.nonterm = {}
        self.word = defaultdict(int)
        self.rare_words = []
        self.q_x_y1y2 = defaultdict(float)
        self.q_x_w = defaultdict(float)

        for line in input:
            parts = line.strip().split(' ')
            count = float(parts[0])
            if parts[1] == 'NONTERMINAL':
                sym = parts[2]
                self.nonterm.setdefault(sym, 0)
                self.nonterm[sym] = count
            elif parts[1] == 'UNARYRULE':
                sym = parts[2]
                word = parts[3]
                self.unary.setdefault((sym, word), 0)
                self.unary[(sym, word)] = count
            elif parts[1] == 'BINARYRULE':
                sym = parts[2]
                y1 = parts[3]
                y2 = parts[4]
                key = (sym, y1, y2)
                self.binary.setdefault(key, 0)
                self.binary[key] = count
        self.count_word()
        self.cal_rule_params()

    def write_params(self, output_file):
        for (x, y1, y2), param in self.q_x_y1y2.iteritems():
            output_file.write('{param} BINARYRULE {x} {y1} {y2}\n'.format(param=param, x=x, y1=y1, y2=y2))

        for (x, w), param in self.q_x_w.iteritems():
            output_file.write('{param} UNARYRULE {x} {w}\n'.format(param=param, x=x, w=w))


class CKYTagger(PCFG):
    def __init__(self):
        super(CKYTagger, self).__init__()

    def tag(self, input, output):
        for line in input:
            result = CKY(line)
            output.write(result)
            output.write('\n')

    def CKY(self, sentence):
        return sentence


def main():
    train_data_filename = 'parse_train.dat'
    train_rare_filename = 'p1.train.rare.dat'
    train_rare_count_filename = 'parser_train.counts.out'

    # count
    pcfg = PCFG()
    for l in open(train_data_filename):
        t = json.loads(l)
        pcfg.count(t)

    # process rare words
    pcfg.count_word()
    process_rare_words(open(train_data_filename),
        open(train_rare_filename, 'w'),
        pcfg.rare_words,
        rare_words_rule_p1)

    # count again
    new_pcfg = PCFG()
    for l in open(train_rare_filename):
        t = json.loads(l)
        new_pcfg.count(t)
    new_pcfg.write(open(train_rare_count_filename, 'w'))

    new_pcfg.cal_rule_params()
    new_pcfg.write_params(open('param.out', 'w'))

if __name__ == '__main__':
    main()
