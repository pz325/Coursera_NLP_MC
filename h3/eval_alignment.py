from __future__ import division
import sys, re, json
from collections import defaultdict

"""
Evaluate a set of test alignments versus the gold set. 
"""


class ParseError(Exception):
  def __init__(self, value):
    self.value = value
    
  def __str__(self):
    return self.value

class FScore:
  "Compute F1-Score based on gold set and test set."

  def __init__(self):
    self.gold = 0
    self.test = 0
    self.correct = 0

  def increment(self, gold_set, test_set):
    "Add examples from sets."
    self.gold += len(gold_set)
    self.test += len(test_set)
    self.correct += len(gold_set & test_set)

  def fscore(self): 
    pr = self.precision() + self.recall()
    if pr == 0: return 0.0
    return (2 * self.precision() * self.recall()) / pr

  def precision(self): 
    if self.test == 0: return 0.0
    return self.correct / self.test

  def recall(self): 
    if self.gold == 0: return 0.0
    return self.correct / self.gold    

  @staticmethod
  def output_header():
    "Output a scoring header."
    print "%10s  %10s  %10s  %10s   %10s"%(
      "Type", "Total", "Precision", "Recall", "F1-Score")
    print "==============================================================="

  def output_row(self, name):
    "Output a scoring row."
    print "%10s        %4d     %0.3f        %0.3f        %0.3f"%(
      name, self.gold, self.precision(), self.recall(), self.fscore())

class CorpusAlignment:
  "Read in the alignment."
  def __init__(self, handle):
    self.all_align = set()
    self.sents_align = {}

    for l in handle:
      t = l.strip().split()
      if len(t) != 3: 
        raise ParseError("Alignment must have three columns. %s"%l)
      try:
        sent = int(t[0])
        align = (int(t[1]), int(t[2]))
        self.all_align.add((sent, align))
      except:
        raise ParseError("Alignment line must be integers. %s"%l)

  @staticmethod
  def compute_fscore(align1, align2):
    fscore = FScore()
    fscore.increment(align1.all_align, align2.all_align)
    return fscore

def main(gold_alignment, test_alignment):
  align1 = CorpusAlignment(gold_alignment)
  align2 = CorpusAlignment(test_alignment)
  fscore = CorpusAlignment.compute_fscore(align1, align2)
  FScore.output_header()
  fscore.output_row("total")
  
if __name__ == "__main__": 
  if len(sys.argv) != 3:
    print >>sys.stderr, """
    Usage: python eval_alignment.py [key_file] [output_file]
        Evalute the accuracy of a output trees compared to a key file.\n"""
    sys.exit(1)
  if sys.argv[1][-4:] != ".key":
    print >>sys.stderr, "First argument should end in '.key'."
    sys.exit(1)
  main(open(sys.argv[1]), open(sys.argv[2])) 

