#!/bin/env/python3
#-*- encdoing: utf-8 -*-
"""

"""
from __future__ import print_function
from __future__ import division
import sys
import os

DEFAULT_NODES = 1

DEFAULT_CORES = 1

DEFAULT_WALLTIME = '1:00:00'

DEFAULT_MEMORY = '8GB'

DEFAULT_CPU = '1:00:00'

DEFAULT_WAIT_TIME = 1


# Maximum number of nodes
MAX_NODES = 5

# Minimum number of nodes
MIN_NODES = 1


MIN_CORES = 1

# Maximum memory that can be allocated to a node
MAX_MEMORY = 96000

# Minimum memory that can be allocated to a node
MIN_MEMORY = 100

# Get ssh username
with open(os.path.join(os.path.dirname(
	os.path.abspath(__file__)),'username.txt'),'r') as f:
	USERNAME = f.read()
