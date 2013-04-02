from p2 import train
from p2 import tag
from pcfg import rare_words_rule_p1


def main():
    TRAIN = True
    train_data_filename = 'parse_train_vert.dat'
    train_rare_filename = 'p3.train.rare.dat'
    pcfg_model_filename = 'p3.model'

    test_data_filename = 'parse_dev.dat'
    result_filename = 'p3.result'

    if TRAIN:
        tagger = train(train_data_filename, train_rare_filename, pcfg_model_filename, rare_words_rule_p1)
        tagger.write(open(pcfg_model_filename, 'w'))

    tag(test_data_filename, result_filename, pcfg_model_filename)

if __name__ == '__main__':
    main()
