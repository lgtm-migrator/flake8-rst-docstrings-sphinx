#!/usr/bin/env python
# This file is managed by 'repo_helper'. Don't edit it directly.

# stdlib
import shutil
import sys

# 3rd party
from setuptools import setup

sys.path.append('.')

# this package
from __pkginfo__ import *  # pylint: disable=wildcard-import

setup(
		description=
		"Extension to flake8-rst-docstrings to filter out warnings related to Sphinx's built in options.",
		extras_require=extras_require,
		install_requires=install_requires,
		py_modules=[],
		version=__version__,
		)

shutil.rmtree("flake8_rst_docstrings_sphinx.egg-info", ignore_errors=True)
