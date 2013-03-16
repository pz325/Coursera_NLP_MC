import util
import p2


def main():
    TRAIN = True
    # 1. training
    hmm_model_filename = 'p3.model'
    train_data_filename = 'gene.train'
    rare_train_data_filename = 'p3.gene.train'
    if TRAIN:
        p2.train(train_data_filename, rare_train_data_filename, hmm_model_filename, util.rare_words_rule_p3)

    # 2. tagging
    test_data_filename = 'gene.dev'
    result_filename = 'gene_dev.p3.output'
    p2.tag(test_data_filename, result_filename, hmm_model_filename)


if __name__ == '__main__':
    main()
