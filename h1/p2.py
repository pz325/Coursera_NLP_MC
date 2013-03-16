from hmm import ViterbiTagger
import util


DEBUG = False


def train(train_data_filename, rare_train_data_filename, hmm_model_filename, rare_words_rule):
    print '1. train hmm model'
    hmm_model = ViterbiTagger(3)
    hmm_model.rare_words_rule = rare_words_rule
    hmm_model.train(file(train_data_filename))

    print '2. process rare words'
    util.process_rare_words(
        file(train_data_filename),
        file(rare_train_data_filename, 'w'),
        hmm_model.rare_words,
        hmm_model.rare_words_rule)

    print '3. train hmm model again using the new train data'
    hmm_model_rare = ViterbiTagger(3)
    hmm_model_rare.train(file(rare_train_data_filename))
    hmm_model_rare.write_counts(file(hmm_model_filename, 'w'))


def tag(test_data_filename, result_filename, hmm_model_filename):
    print '1. load Hmm model'
    tagger = ViterbiTagger(3)
    tagger.read_counts(file(hmm_model_filename))

    print '2. tag test file'
    tagger.tag(file(test_data_filename), file(result_filename, 'w'))


def main():
    TRAIN = True
    # 1. training
    hmm_model_filename = 'p2.model'
    train_data_filename = 'gene.train'
    rare_train_data_filename = 'p2.gene.train'
    if TRAIN:
        train(train_data_filename, rare_train_data_filename, hmm_model_filename, util.rare_words_rule_p1)

    # 2. tagging
    test_data_filename = 'gene.dev'
    result_filename = 'gene_dev.p2.output'
    tag(test_data_filename, result_filename, hmm_model_filename)

if __name__ == '__main__':
    main()
