#!/usr/bin/env python
#-*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function
from __future__ import division
import numpy as np 
import argparse
import sys
import os

root_dir = os.path.dirname(os.path.abspath(__file__))

if not root_dir in sys.path:
	sys.path.append(root_dir)

import server
import client
from helper_functions import *


def setup_server():
	pass

def setup_client():
	pass

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-r","--root",action='store_true',
		help="Call to create a root node")

	parser.add_argument("-sr","--sub-root",action='store_true',
		help="Call to create a root node")

	parser.add_argument("-n","--node",action='store_true',
		help="Call to create a root node")

	args = parser.parse_args()
	print(args)

if __name__ == "__main__":
	main()