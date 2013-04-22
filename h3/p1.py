from ibmmodel import IBMModel1


def main():
    TRAIN = False
    corpus_e = 'corpus.en'
    corpus_f = 'corpus.es'
    target_e = 'dev.en'
    target_f = 'dev.es'
    t_filename = 'model1'

    model1 = IBMModel1()
    if TRAIN:
        model1.count(corpus_e, corpus_f)
        model1.EM(corpus_e, corpus_f)
        model1.save_t(open(t_filename, 'w'))
        # model1.print_t()
    else:
        model1.load_t(open(t_filename))
        # model1.print_t()

    model1.align(target_e, target_f)
    model1.save_a(open('p1.out', 'w'))


if __name__ == '__main__':
    main()
