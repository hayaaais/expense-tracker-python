import os
import sys

# Allow tests to import modules from the project root (one level up from tests/)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
