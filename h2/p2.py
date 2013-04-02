import json
from pcfg import PCFG
from pcfg import CKYTagger
from pcfg import process_rare_words
from pcfg import rare_words_rule_p1


def train(train_data_filename, train_rare_filename, pcfg_model_filename, rare_words_rule):
    print 'train PCFG model'
    pcfg = PCFG()
    for l in open(train_data_filename):
        t = json.loads(l)
        pcfg.count(t)
    pcfg.count_word()

    print 'process rare word'
    process_rare_words(open(train_data_filename),
        open(train_rare_filename, 'w'),
        pcfg.rare_words,
        rare_words_rule)

    print 'train PCFG model again'
    new_pcfg = PCFG()
    for l in open(train_rare_filename):
        t = json.loads(l)
        new_pcfg.count(t)
    new_pcfg.cal_rule_params()

    new_pcfg.write(open(pcfg_model_filename, 'w'))
    return new_pcfg


def tag(test_data_filename, result_filename, pcfg_model_filename):
    print 'load PCFG model'
    tagger = CKYTagger()
    tagger.read(open(pcfg_model_filename))
    # tagger.write_params(open('param', 'w'))
    tagger.tag(open(test_data_filename), open(result_filename, 'w'))
    pass


def main():
    TRAIN = True
    train_data_filename = 'parse_train.dat'
    train_rare_filename = 'p2.train.rare.dat'
    pcfg_model_filename = 'p2.model'
    # train_rare_count_filename = 'parser_train.counts.out'

    test_data_filename = 'parse_dev.dat'
    # test_data_filename = 'one_sent_test.dat'
    result_filename = 'p2.result'

    if TRAIN:
        tagger = train(train_data_filename, train_rare_filename, pcfg_model_filename, rare_words_rule_p1)
        tagger.write(open(pcfg_model_filename, 'w'))

    tag(test_data_filename, result_filename, pcfg_model_filename)

if __name__ == '__main__':
    main()
