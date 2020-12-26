#!/usr/bin/env python3
#
#  domains.py
"""
Different Sphinx domains, controlling the permitted roles and directives.
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
from typing import Set

__all__ = ["Autodoc", "Builtin", "Domain", "Python", "Rest", "Toolbox"]


class Domain:
	"""
	Represents a Sphinx domain.
	"""

	roles: Set[str] = set()
	directives: Set[str] = set()

	def __init__(self):
		self.roles = set(self.roles)
		self.directives = set(self.directives)


class Python(Domain):
	"""
	Represents the roles and directives in Sphinx's Python domain.
	"""

	def __init__(self):
		super().__init__()

		# Sphinx Python domain
		python_domain_directives = {
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
				}
		self.directives.update(python_domain_directives)
		self.directives.update(f"py:{x}" for x in python_domain_directives)

		python_domain_roles = ["mod", "func", "data", "const", "class", "meth", "attr", "exc", "obj"]
		self.roles.update(python_domain_roles)
		self.roles.update(f"py:{x}" for x in python_domain_roles)


class Rest(Domain):
	"""
	Represents the roles and directives in Sphinx's reST domain.
	"""

	def __init__(self):
		super().__init__()

		# Sphinx reST domain
		self.directives.update(f"rst:{x}" for x in ["directive", "directive:option", "role"])
		self.roles.update(f"rst:{x}" for x in ["dir", "role"])


class Builtin(Python, Rest):
	"""
	Represents Sphinx's builtin roles and directives.
	"""

	def __init__(self):
		Python.__init__(self)
		Rest.__init__(self)

		self.roles.update({
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
				})
		self.directives.update({
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
				})


class Autodoc(Builtin):
	"""
	Represents the roles and directives added by autodoc.
	"""

	def __init__(self):
		super().__init__()
		self.directives.update(("autoclass", "autofunction", "autodata", "automethod"))


class Toolbox(Autodoc):
	"""
	Represents the roles and directives added by `sphinx-toolbox <https://sphinx-toolbox.readthedocs.io>`_ .
	"""

	def __init__(self):
		super().__init__()

		self.roles.update(["wikipedia", "pull", "issue", "asset", "confval", "data", "deco", "regex"])

		self.directives.update([
				"rest-example",
				"extensions",
				"confval",
				"pre-commit-shield",
				"prompt",
				])
