import json
from pcfg import PCFG
from pcfg import process_rare_words
from pcfg import rare_words_rule_p1


def main():
    train_data_filename = 'parse_train.dat'
    train_rare_filename = 'p1.train.rare.dat'
    pcfg_model_filename = 'parser_train.counts.out'

    pcfg = PCFG()
    for l in open(train_data_filename):
        t = json.loads(l)
        pcfg.count(t)
    pcfg.count_word()

    process_rare_words(open(train_data_filename),
        open(train_rare_filename, 'w'),
        pcfg.rare_words,
        rare_words_rule_p1)

    new_pcfg = PCFG()
    for l in open(train_rare_filename):
        t = json.loads(l)
        new_pcfg.count(t)
    new_pcfg.cal_rule_params()

    new_pcfg.write(open(pcfg_model_filename, 'w'))

if __name__ == '__main__':
    main()
