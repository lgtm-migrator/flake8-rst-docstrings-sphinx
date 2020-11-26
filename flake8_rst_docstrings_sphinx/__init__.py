#!/usr/bin/env python3
#
#  __init__.py
"""
Extension to flake8-rst-docstrings to filter out warnings related to Sphinx's built in options.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#

# stdlib
import re
from configparser import ConfigParser
from functools import partial
from gettext import ngettext
from typing import List, Optional

# this package
from flake8_rst_docstrings_sphinx.domains import Autodoc, Builtin, Domain, Toolbox

__all__ = ["compile_options"]

__author__ = "Dominic Davis-Foster"
__copyright__ = "2020 Dominic Davis-Foster"
__license__ = "MIT"
__version__ = "0.0.0"
__email__ = "dominic@davis-foster.co.uk"

_error = partial(ngettext, "error", "errors")
_file = partial(ngettext, "file", "files")


def compile_options(
		rst_roles: Optional[List[str]],
		rst_directives: Optional[List[str]],
		*,
		allow_autodoc: bool = False,
		allow_toolbox: bool = False,
		):
	"""
	Compile the list of allowed roles and directives.

	:param rst_roles:
	:param rst_directives:
	:param allow_autodoc:
	:param allow_toolbox:
	"""

	default_allowed_rst_directives = []
	default_allowed_rst_roles = []

	config = ConfigParser()
	config.read("tox.ini")

	if "flake8" in config:
		if "rst-directives" in config["flake8"]:
			default_allowed_rst_directives.extend(re.split(r"[\n,]", config["flake8"]["rst-directives"]))
		if "rst-roles" in config["flake8"]:
			default_allowed_rst_roles.extend(re.split(r"[\n,]", config["flake8"]["rst-roles"]))

	domain: Domain

	if allow_toolbox:
		domain = Toolbox()
	elif allow_autodoc:
		domain = Autodoc()
	else:
		domain = Builtin()

	if rst_roles is None:
		rst_roles = sorted({*default_allowed_rst_roles, *domain.roles})

	if rst_directives is None:
		rst_directives = sorted({*default_allowed_rst_directives, *domain.directives})

	return rst_roles, rst_directives
