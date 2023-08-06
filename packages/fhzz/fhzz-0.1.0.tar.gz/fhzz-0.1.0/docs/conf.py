import os
import sys
sys.path.insert(0, os.path.abspath("../src"))

import fhzz

project = 'fhzz'
copyright = "2023, zluudg"
author = 'zluudg'
release = 'fhzz.__version__'
version = 'fhzz.__version__'

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]
templates_path = ['_templates']
exclude_patterns = ["dist", ".tox", ".pytest_cache", "build", "venv"]

html_theme = 'alabaster'
html_static_path = ['_static']

nitpicky = True
