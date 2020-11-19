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
#  "Application" based on Flake8
#  Copyright (C) 2011-2013 Tarek Ziade <tarek@ziade.org>
#  Copyright (C) 2012-2016 Ian Cordasco <graffatcolmingov@gmail.com>
#  MIT Licensed
#

# stdlib
import re
from configparser import ConfigParser
from functools import partial
from gettext import ngettext
from typing import List, Optional, Tuple

# 3rd party
import click
import flake8.main.application  # type: ignore

# this package
from flake8_rst_docstrings_sphinx.domains import Autodoc, Builtin, Toolbox

__all__ = ["Application", "compile_options"]

__author__ = "Dominic Davis-Foster"
__copyright__ = "2020 Dominic Davis-Foster"
__license__ = "MIT"
__version__ = "0.0.0"
__email__ = "dominic@davis-foster.co.uk"

_error = partial(ngettext, "error", "errors")
_file = partial(ngettext, "file", "files")


class Application(flake8.main.application.Application):
	"""
	Subclass of Flake8's ``Application``.
	"""

	def exit(self) -> None:
		"""
		Handle finalization and exiting the program.

		This should be the last thing called on the application instance.
		It will check certain options and exit appropriately.
		"""

		if self.options.count:
			files_checked = self.file_checker_manager.statistics["files"]
			files_with_errors = self.file_checker_manager.statistics["files_with_errors"]
			if self.result_count:
				click.echo(
						f"Found {self.result_count} {_error(self.result_count)} "
						f"in {files_with_errors} {_file(files_with_errors)} "
						f"(checked {files_checked} source {_file(files_checked)})"
						)
			else:
				click.echo(f"Success: no issues found in {files_checked} source {_file(files_checked)}")

		if self.options.exit_zero:
			raise SystemExit(self.catastrophic_failure)
		else:
			raise SystemExit((self.result_count > 0) or self.catastrophic_failure)

	def report_errors(self) -> None:
		"""
		Report all the errors found by flake8 3.0.

		This also updates the :attr:`result_count` attribute with the total
		number of errors, warnings, and other messages found.
		"""

		flake8.main.application.LOG.info("Reporting errors")

		files_with_errors = results_reported = results_found = 0

		for checker in self.file_checker_manager._all_checkers:
			results_ = sorted(checker.results, key=lambda tup: (tup[1], tup[2]))
			filename = checker.display_name

			with self.file_checker_manager.style_guide.processing_file(filename):
				results_reported_for_file = self.file_checker_manager._handle_results(filename, results_)
				if results_reported_for_file:
					results_reported += results_reported_for_file
					files_with_errors += 1

			results_found += len(results_)

		results: Tuple[int, int] = (results_found, results_reported)

		self.total_result_count, self.result_count = results
		flake8.main.application.LOG.info(
				"Found a total of %d violations and reported %d",
				self.total_result_count,
				self.result_count,
				)

		self.file_checker_manager.statistics["files_with_errors"] = files_with_errors


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

	if allow_toolbox:
		domain = Toolbox()
	elif allow_autodoc:
		domain = Autodoc()
	else:
		domain = Builtin()

	if rst_roles is None:
		rst_roles = sorted({*default_allowed_rst_roles, domain.roles})

	if rst_directives is None:
		rst_directives = sorted({*default_allowed_rst_directives, domain.directives})

	return rst_roles, rst_directives
