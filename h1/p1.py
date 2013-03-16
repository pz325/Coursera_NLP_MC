from hmm import Hmm_ex
from util import *


def train(train_data_filename, rare_train_data_filename, hmm_model_filename):
    print '1. train hmm model'
    hmm_model = Hmm_ex(3)
    hmm_model.train(file(train_data_filename, 'r'))

    print '2. replace rare words'
    rare_words = hmm_model.rare_words
    process_rare_words(file(train_data_filename), file(rare_train_data_filename, 'w'), rare_words, rare_words_rule_p1)

    print '3. train hmm model again using the new train data (with RARE_TAG)'
    hmm_model_rare = Hmm_ex(3)
    hmm_model_rare.train(file(rare_train_data_filename))
    hmm_model_rare.write_counts(file(hmm_model_filename, 'w'))


def tag(test_data_filename, result_filename, hmm_model_filename):
    print '1. load Hmm model'
    tagger = SimpleTagger(3)
    tagger.read_counts(file(hmm_model_filename))

    print '2. tag test file'
    tagger.tag(test_data_filename, result_filename)


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
            e = self.emission_params[(RARE_TAG, tag)]
            if e > max_e_rare_y:
                max_e_rare_y, max_rare_y = e, tag
        # load test_data
        word_iterator = test_data_iterator(file(test_data_filename))
        # tag
        for word in word_iterator:
            max_e, max_y = -1.0, ''
            if word is not None:
                if word == RARE_TAG or word not in self.words:
                    max_y = max_rare_y
                else:
                    for tag in self.tags:
                        e = self.emission_params[(word, tag)]
                        if e > max_e:
                            max_e, max_y = e, tag
                output.write('{0} {1}\n'.format(word, max_y))
            else:
                output.write('\n')


def main():
    TRAIN = False
    # 1. training
    hmm_model_filename = 'p1.model'
    train_data_filename = 'gene.train'
    rare_train_data_filename = 'p1.gene.train'
    if TRAIN:
        train(train_data_filename, rare_train_data_filename, hmm_model_filename)

    # 2. tagging
    test_data_filename = 'gene.dev'
    result_filename = 'gene_dev.p1.output'
    tag(test_data_filename, result_filename, hmm_model_filename)

if __name__ == '__main__':
    main()
