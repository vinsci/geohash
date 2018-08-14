
from __future__ import print_function

import os
import sys

# Test the source tree, not an installed version.
os.chdir('..')
sys.path.insert(0, os.getcwd())

if __name__ == '__main__':
    import doctest
    print("Testing tests in README.rst...")
    doctest.testfile('./README.rst')
