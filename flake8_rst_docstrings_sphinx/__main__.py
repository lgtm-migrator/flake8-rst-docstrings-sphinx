#!/usr/bin/env python3
#
#  __main__.py
"""
CLI entry point.
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
import sys
from configparser import ConfigParser
from functools import partial
from gettext import ngettext
from typing import List, Optional, Tuple

# 3rd party
import click
import flake8.main.application  # type: ignore
from click import Context
from consolekit import CONTEXT_SETTINGS
from consolekit.options import MultiValueOption

# this package
from flake8_rst_docstrings_sphinx import AutodocFormatter, Formatter, ToolboxFormatter

__all__ = ["main"]

_error = partial(ngettext, "error", "errors")
_file = partial(ngettext, "file", "files")


class Application(flake8.main.application.Application):
	"""
	Subclass of Flake8's ``Application``.
	"""

	def exit(self) -> None:  # noqa: A003  # pylint: disable=redefined-builtin
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

	if rst_roles is None:
		if allow_toolbox:
			rst_roles = sorted({*default_allowed_rst_roles, *ToolboxFormatter.allowed_rst_roles})
		elif allow_autodoc:
			rst_roles = sorted({*default_allowed_rst_roles, *AutodocFormatter.allowed_rst_roles})
		else:
			rst_roles = sorted({*default_allowed_rst_roles, *Formatter.allowed_rst_roles})

	if rst_directives is None:
		if allow_toolbox:
			rst_directives = sorted({*default_allowed_rst_directives, *ToolboxFormatter.allowed_rst_directives})
		elif allow_autodoc:
			rst_directives = sorted({*default_allowed_rst_directives, *AutodocFormatter.allowed_rst_directives})
		else:
			rst_directives = sorted({*default_allowed_rst_directives, *Formatter.allowed_rst_directives})

	return rst_roles, rst_directives


@click.option(
		"--rst-roles",
		type=click.STRING,
		default=None,
		cls=MultiValueOption,
		help="List of roles to allow instead of the default",
		)
@click.option(
		"--rst-directives",
		type=click.STRING,
		default=None,
		cls=MultiValueOption,
		help="List of directives to allow instead of the default",
		)
@click.option(
		"--disallow-sphinx",
		is_flag=True,
		default=False,
		help="Don't allow any sphinx roles and directives (function like vanilla Flake8)",
		)
@click.option(
		"--allow-autodoc",
		is_flag=True,
		default=False,
		help="Whether to allow autodoc's roles and directives.",
		)
@click.option(
		"--allow-toolbox",
		is_flag=True,
		default=False,
		help="Whether to allow sphinx-toolbox's roles and directives. Implies '--allow-autodoc'.",
		)
@click.command(context_settings={"ignore_unknown_options": True, "allow_extra_args": True, **CONTEXT_SETTINGS})
@click.pass_context
def main(
		ctx: Context,
		rst_directives: List[str],
		rst_roles: List[str],
		disallow_sphinx: bool,
		allow_autodoc: bool,
		allow_toolbox: bool,
		):
	"""
	Wrapper around flake8 and flake8-rst-docstrings to filter out warnings related to Sphinx's built in options.
	"""

	unknown = ctx.args[:]

	rst_roles, rst_directives = compile_options(
		rst_roles,
		rst_directives,
		allow_autodoc=allow_autodoc,
		allow_toolbox=allow_toolbox,
		)

	if not disallow_sphinx:
		unknown.append(f"--rst-directives=" + ','.join(rst_directives))
		unknown.append(f"--rst-roles=" + ','.join(rst_roles))

	app = Application()
	app.run(unknown)
	app.exit()


if __name__ == "__main__":
	sys.exit(main(obj={}))
