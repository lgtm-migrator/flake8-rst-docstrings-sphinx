#!/usr/bin/env python3
#
#  __main__.py
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
import sys
from typing import List

# 3rd party
import click
from consolekit import CONTEXT_SETTINGS
from consolekit.options import MultiValueOption

__all__ = ["main"]

# this package
from flake8_rst_docstrings_sphinx import Application, compile_options


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
		ctx: click.Context,
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
