# -*- coding: utf-8 -*-
import sys
import re

DEBUG = False
NUMERIC_TAG = '_NUMERIC_'
ALL_UPPERCASE_TAG = '_ALLUPPERCASE_'
LAST_UPPERCASE_TAG = '_LASTUPPERCASE_'
RARE_TAG = '_RARE_'
RARE_WORD_THRESHOLD = 5


def is_numeric(word):
    '''
    the word contains at least one numeric characters
    '''
    find_numeric = False
    if re.match('[0-9]+', word):
        find_numeric = True
    # for c in word:
    #     try:
    #         int(c)
    #         find_numeric = True
    #         break
    #     except ValueError:
    #         continue
    return find_numeric


def is_all_uppercase(word):
    '''
    The word consists entirely of capitalized letters.
    '''
    all_uppercase = False
    if re.match('^[A-Z]+$', word):
        all_uppercase = True
    # for c in word:
    #     if not c.isupper():
    #         all_uppercase = False
    #         break
    return all_uppercase


def is_last_uppercase(word):
    '''
    The word is rare, not all capitals, and ends with a capital letter.
    '''
    last_uppercase = False
    if re.match('.*[A-Z]$', word):
        last_uppercase = True
    return last_uppercase
    # return word[-1].isupper()


def rare_words_rule_p1(word):
    '''
    Replace infrequent words (Count(x) < 5) with a common symbol RARE .
    '''
    return RARE_TAG


def rare_words_rule_p3(word):
    '''
    applying the rule required by Part 3 to process the training data:

    Numeric The word is rare and contains at least one numeric characters.
    All Capitals The word is rare and consists entirely of capitalized letters.
    Last Capital The word is rare, not all capitals, and ends with a capital letter.
    Rare The word is rare and does not ﬁt in the other classes
    '''
    w = RARE_TAG
    if is_numeric(word):
        w = NUMERIC_TAG
    # else:
    if is_all_uppercase(word):
        w = ALL_UPPERCASE_TAG
    if is_last_uppercase(word):
        w = LAST_UPPERCASE_TAG
    return w


def process_rare_words(input_file, output_file, rare_words, processer):
    """
    applying the rare word rule to process the training data
    """
    l = input_file.readline()
    while l:
        line = l.strip()
        if line:
            fields = line.split(' ')
            word = fields[0]
            tag = fields[-1]
            if word in rare_words:
                if DEBUG:
                    print 'rare word: {word}, TAG: {tag}'.format(word=word, tag=processer(word))
                word = processer(word)  # applying rare word rule(s)
            output_file.write('{0} {1}\n'.format(word, tag))
        else:
            output_file.write('\n')
        l = input_file.readline()


def test_data_iterator(test_file):
    """
    return an iterator object that yields one word at a time from test_file
    test_file has a word each line, sentence breaks by an empty line
    """
    l = test_file.readline()
    while l:
        line = l.strip()
        if line:
            yield line  # a word
        else:
            yield None  # end of a line
        l = test_file.readline()


def test_sent_iterator(testdata_iterator):
    """
    return an iterator object that yields one sent at a time
    """
    current_sentence = []  # Buffer for the current sentence
    for word in testdata_iterator:
            if word is None:
                if current_sentence:  # Reached the end of a sentence
                    yield current_sentence
                    current_sentence = []  # Reset buffer
                else:  # Got empty input stream
                    sys.stderr.write("WARNING: Got empty input file/stream.\n")
                    raise StopIteration
            else:
                current_sentence.append(word)  # Add token to the buffer

    if current_sentence:  # If the last line was blank, we're done
        yield current_sentence   # Otherwise when there is no more token
                                # in the stream return the last sentence.


def test():
    print is_last_uppercase('DDDeD')


if __name__ == '__main__':
    test()
