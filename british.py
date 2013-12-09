#! /usr/env/python

# run this wil along with simple_test.txt in python shell to test parser

import sys
from british_tokenizer import *
import british_tokenizer

if __name__ == '__main__':
	filename = sys.argv[1]
	file = open(filename)
	characters = file.read()
	file.close()

	british_tokenize(characters)
	try:
		tree = parse()
	except:
		print british_tokenizer.tokens
		raise
	tree.eval()
	# print british_tokenizer.global_env

