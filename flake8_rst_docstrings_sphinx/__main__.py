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
import re
import sys
from argparse import ArgumentParser
from configparser import ConfigParser
from typing import List, Optional

# 3rd party
import flake8.main.cli  # type: ignore

# this package
from flake8_rst_docstrings_sphinx import AutodocFormatter, Formatter, ToolboxFormatter

__all__ = ["main"]


def main(argv: Optional[List[str]] = None) -> None:
	default_allowed_rst_directives = []
	default_allowed_rst_roles = []

	config = ConfigParser()
	config.read("tox.ini")

	if "flake8" in config:
		if "rst-directives" in config["flake8"]:
			default_allowed_rst_directives.extend(re.split(r"[\n,]", config["flake8"]["rst-directives"]))
		if "rst-roles" in config["flake8"]:
			default_allowed_rst_roles.extend(re.split(r"[\n,]", config["flake8"]["rst-roles"]))

	parser = ArgumentParser()
	parser.add_argument("--rst-directives", type=list, default=None)  # type: ignore
	parser.add_argument("--rst-roles", type=list, default=None)  # type: ignore
	parser.add_argument("--disallow-sphinx", action="store_true", default=False)
	parser.add_argument("--allow-autodoc", action="store_true", default=False)
	parser.add_argument("--allow-toolbox", action="store_true", default=False)  # implies allow-autodoc

	if argv is None:
		argv = sys.argv[1:]

	args, unknown = parser.parse_known_args(argv)

	if args.rst_roles is None:
		if args.allow_toolbox:
			args.rst_roles = sorted({*default_allowed_rst_roles, *ToolboxFormatter.allowed_rst_roles})
		elif args.allow_autodoc:
			args.rst_roles = sorted({*default_allowed_rst_roles, *AutodocFormatter.allowed_rst_roles})
		else:
			args.rst_roles = sorted({*default_allowed_rst_roles, *Formatter.allowed_rst_roles})

	if args.rst_directives is None:
		if args.allow_toolbox:
			args.rst_directives = sorted({
					*default_allowed_rst_directives, *ToolboxFormatter.allowed_rst_directives
					})
		elif args.allow_autodoc:
			args.rst_directives = sorted({
					*default_allowed_rst_directives, *AutodocFormatter.allowed_rst_directives
					})
		else:
			args.rst_directives = sorted({*default_allowed_rst_directives, *Formatter.allowed_rst_directives})

	if not args.disallow_sphinx:
		unknown.append(f"--rst-directives=" + ','.join(args.rst_directives))
		unknown.append(f"--rst-roles=" + ','.join(args.rst_roles))

	flake8.main.cli.main(unknown)


if __name__ == "__main__":
	main(sys.argv[1:])
