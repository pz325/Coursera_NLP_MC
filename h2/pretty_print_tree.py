#! /usr/bin/python

import sys, json, pprint

"""
Pretty print a tree from json.
"""

'''Extending pprint'''

class Node: 
  """
  Dummy class for python's pretty printer.
  """
  def __init__(self, name): self.name = name 
  def __repr__(self): return self.name

def format_tree(tree):
  """
  Convert a tree with strings, to one with nodes.
  """
  tree[0] = Node(tree[0])
  if len(tree) == 2: 
    tree[1] = Node(tree[1])
  elif len(tree) == 3: 
    format_tree(tree[1])
    format_tree(tree[2])

def pretty_print_tree(tree):
  """
  Print out a tree with nice formatting.
  """
  format_tree(tree)
  print pprint.pformat(tree)

def main(parse_file):
  for l in open(parse_file):
    pretty_print_tree(json.loads(l))
    

def usage():
    sys.stderr.write("""
    Usage: python pretty_print_tree.py [tree_file]
        Pretty print a file of trees.\n""")

if __name__ == "__main__": 
  if len(sys.argv) != 2:
    usage()
    sys.exit(1)
  main(sys.argv[1])
