from collections import defaultdict


class Count(object):
    """docstring for ClassName"""
    def __init__(self):
        self.t = defaultdict()

    def count(self, corpus_e, corpus_f):
        self.t = defaultdict()
        self.t['NULL'] = defaultdict(int)
        for e_line, f_line in zip(open(corpus_e), open(corpus_f)):
            e_words = e_line.strip().split(' ')
            f_words = f_line.strip().split(' ')
            for e in e_words:
                if e not in self.t:
                    self.t[e] = defaultdict(int)
                for f in f_words:
                    self.t[e][f] += 1
            for f in f_words:
                self.t['NULL'][f] += 1

    def print_t(self):
        for e in self.t:
            for f in self.t[e]:
                print 't({f} | {e}) = {t}'.format(f=f, e=e, t=self.t[e][f])

    def print_n(self):
        for e in self.t:
            print 'n({e})={n_e}'.format(e=e, n_e=len(self.t[e]))

    def save_t(self, output):
        for e in self.t:
            for f in self.t[e]:
                output.write('{e} {f} {t}'.format(e=e, f=f, t=self.t[e][f]))
                output.write('\n')

    def load_t(self, input):
        self.t = defaultdict()
        for line in input:
            items = line.strip().split(' ')
            if len(items) < 3:
                continue
            e = items[0]
            f = items[1]
            t = float(items[2])
            if e not in self.t:
                self.t[e] = defaultdict(int)
            self.t[e][f] = t


class IBMModel1(Count):
    def __init__(self):
        super(Count, self).__init__()
        self.num_iteration = 5
        self.c = defaultdict(float)

    def _init(self):
        for e in self.t:
            n_e = len(self.t[e])
            for f in self.t[e]:
                self.t[e][f] = 1.0 / float(n_e)

    def _max(self, corpus_e, corpus_f):
        self.c = defaultdict(float)
        for e_line, f_line in zip(corpus_e, corpus_f):
            e_words = e_line.strip().split(' ')
            f_words = f_line.strip().split(' ')
            e_words = ['NULL'] + e_words
            for f in f_words:
                # calculate sum
                sum_t = 0.0
                for e in e_words:
                    sum_t += self.t[e][f]
                for e in e_words:
                    delta = self.t[e][f] / sum_t
                    self.c[(e, f)] += delta
                    self.c[e] += delta

    def _expect(self):
        for e in self.t:
            for f in self.t[e]:
                self.t[e][f] = self.c[(e, f)] / self.c[e]

    def EM(self, corpus_e_filename, corpus_f_filename):
        self._init()
        for i in xrange(0, self.num_iteration):
            print 'iteration', i+1
            self._max(open(corpus_e_filename), open(corpus_f_filename))
            # self.print_c()
            self._expect()

    def align(self, targeting_e_filename, targeting_f_filename):
        self.a = []
        k = 1
        for e_line, f_line in zip(open(targeting_e_filename), open(targeting_f_filename)):
            e_words = e_line.strip().split(' ')
            f_words = f_line.strip().split(' ')
            e_words = ['NULL'] + e_words
            i = 1
            for f in f_words:
                j = 0
                max_t = -1
                a_i = j
                for e in e_words:
                    if self.t[e][f] > max_t:
                        max_t = self.t[e][f]
                        a_i = j
                    j += 1
                self.a.append([k, a_i, i])
                i += 1
            k += 1

    def print_c(self):
        for k in self.c:
            print 'c({key}) = {c}'.format(key=k, c=self.c[k])

    def save_a(self, output):
        for l in self.a:
            output.write('{s_index} {e_index} {f_index}'.format(s_index=l[0], e_index=l[1], f_index=l[2]))
            output.write('\n')


def main():
    pass

if __name__ == '__main__':
    main()
