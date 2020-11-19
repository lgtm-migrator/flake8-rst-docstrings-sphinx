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
from typing import Optional

# 3rd party
from flake8.formatting.base import BaseFormatter  # type: ignore
from flake8.style_guide import Violation  # type: ignore

__all__ = ["Formatter", "AutodocFormatter", "ToolboxFormatter"]

__author__ = "Dominic Davis-Foster"
__copyright__ = "2020 Dominic Davis-Foster"
__license__ = "MIT"
__version__ = "0.0.0"
__email__ = "dominic@davis-foster.co.uk"


class Formatter(BaseFormatter):

	error_format = "%(path)s:%(row)d:%(col)d: %(code)s %(text)s"

	allow_autodoc = False
	allow_toolbox = False

	allowed_rst_roles = []

	# Sphinx built in
	allowed_rst_roles.extend([
			"any",
			"ref",
			"doc",
			"download",
			"numref",
			"envvar",
			"keyword",
			"option",
			"term",
			"math",
			"eq",
			"abbr",
			"command",
			"dfn",
			"file",
			"guilabel",
			"kbd",
			"mailheader",
			"menuselection",
			"mimetype",
			"samp",
			"pep",
			"rfc",
			"index",
			])

	allowed_rst_directives = []

	# Sphinx built in
	allowed_rst_directives.extend([
			"toctree",
			"note",
			"warning",
			"versionadded",
			"versionchanged",
			"deprecated",
			"seealso",
			"rubric",
			"centered",
			"hlist",
			"highlight",
			"code-block",
			"literalinclude",
			"glossary",
			"sectionauthor",
			"codeauthor",
			"index",
			"only",
			"tabularcolumns",
			"math",
			"productionlist",
			])

	# Sphinx Python domain
	python_domain_directives = [
			"module",
			"function",
			"data",
			"exception",
			"class",
			"attribute",
			"method",
			"staticmethod",
			"classmethod",
			"decorator",
			"decoratormethod",
			]
	allowed_rst_directives.extend(python_domain_directives)
	allowed_rst_directives.extend(f"py:{x}" for x in python_domain_directives)

	# Sphinx reST domain
	allowed_rst_directives.extend(f"rst:{x}" for x in ["directive", "directive:option", "role"])

	# Sphinx Python domain
	python_domain_roles = ["mod", "func", "data", "const", "class", "meth", "attr", "exc", "obj"]
	allowed_rst_roles.extend(python_domain_roles)
	allowed_rst_roles.extend(f"py:{x}" for x in python_domain_roles)

	# Sphinx reST domain
	allowed_rst_roles.extend(f"rst:{x}" for x in ["dir", "role"])

	def handle(self, error: Violation):

		if error.code == "RST304":
			m = re.match(r'Unknown interpreted text role "(.*)"\.', error.text)
			if m:
				if m.group(1) in self.allowed_rst_roles:
					return

		elif error.code == "RST303":
			m = re.match(r'Unknown directive type "(.*)"\.', error.text)
			if m:
				if m.group(1) in self.allowed_rst_directives:
					return

		super().handle(error)

	def format(self, error: Violation) -> Optional[str]:
		"""
		Format and write error out.

		If an output filename is specified, write formatted errors to that
		file. Otherwise, print the formatted error to standard out.
		"""

		return self.error_format % {
				"code": error.code,
				"text": error.text,
				"path": error.filename,
				"row": error.line_number,
				"col": error.column_number,
				}


class AutodocFormatter(Formatter):

	allow_autodoc = True

	allowed_rst_directives = [
			*Formatter.allowed_rst_directives, "autoclass", "autofunction", "autodata", "automethod"
			]


class ToolboxFormatter(AutodocFormatter):

	allow_toolbox = True

	allowed_rst_roles = [
			*AutodocFormatter.allowed_rst_roles,
			"wikipedia",
			"pull",
			"issue",
			"asset",
			"confval",
			"data",
			"deco",
			"regex"
			]

	allowed_rst_directives = [
			*AutodocFormatter.allowed_rst_directives,
			"rest-example",
			"extensions",
			"confval",
			"pre-commit-shield",
			"prompt",
			]
