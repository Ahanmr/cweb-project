from __future__ import absolute_import
import sys
import os

base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_path)

from cloudpickle import *

__version__ = '0.6.1'
