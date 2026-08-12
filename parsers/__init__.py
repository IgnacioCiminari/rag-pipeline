# This file makes parsers a Python module
import sys
import os

engines_path = os.path.join(os.path.dirname(__file__), "engines")
if engines_path not in sys.path:
    sys.path.insert(0, engines_path)
