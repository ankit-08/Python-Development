# tests/conftest.py
# Ensure tests can import the package under the project root
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
