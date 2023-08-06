# package_smoke_test/__main__.py
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Post-install Python smoke test for use in Debian AutoPkgTest.

    Written to test the installed version of a package.

    Smoke test the distribution::
        --distribution=DISTRIBUTION

    Smoke test one or more modules::
        --module=MODULE_FOO --module=MODULE_BAR --module=MODULE_BAZ
    """

import argparse
import importlib
import importlib.metadata
import sys
import textwrap


def emit_implementation():
    """ Emit the details of the current Python implementation.

        :return: ``None``.
        """
    sys.stdout.write(textwrap.dedent("""\
            Interpreter: {command}
            \t{version}
            """).format(command=sys.executable, version=sys.version))


def emit_distribution_metadata(name):
    """ Get the distribution `name` and emit some metadata.

        :param name: Name of the distribution to retrieve.
        :return: ``None``.
        """
    metadata = importlib.metadata.metadata(name)
    sys.stdout.write(textwrap.dedent("""\
            Distribution ‘{name}’:
            \t{metadata[Name]} {metadata[Version]}
            """).format(name=name, metadata=metadata))


def emit_module(name):
    """ Import the module `name` and emit the module representation.

        :param name: Full name of the module to import.
        :return: ``None``.
        """
    module = importlib.import_module(name)
    sys.stdout.write(textwrap.dedent("""\
            Module ‘{name}’:
            \t{module!r}
            """).format(name=name, module=module))


def suite(args):
    """ Run the full suite of tests.

        :param args: Namespace of arguments parsed from `ArgumentParser`.
        :return: ``None``.
        """
    emit_implementation()

    if args.distribution_name:
        emit_distribution_metadata(args.distribution_name)

    if args.module_names:
        for module_name in args.module_names:
            emit_module(module_name)


class SmokeTestArgumentParser(argparse.ArgumentParser):
    """ Command-line argument parser for this program. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_argument(
                '--distribution',
                dest='distribution_name', type=str,
                metavar="DISTRIBUTION", help=(
                    "Test the Python distribution named DISTRIBUTION."))
        self.add_argument(
                '--module',
                dest='module_names', type=str, nargs='+',
                metavar="MODULE", help=(
                    "Test the Python module named MODULE."))

    def parse_args(self, *args, **kwargs):
        args = super().parse_args(*args, **kwargs)

        if (not any([args.distribution_name, args.module_names])):
            self.error("one of DISTRIBUTION or MODULE is required")

        return args


def main(argv=None):
    """ Mainline code for this module.

        :param argv: Sequence of all command line arguments.
            (Default: `sys.argv`)
        :return: The exit status (integer) for exit from the process.
        """
    exit_status = 0

    if argv is None:
        argv = sys.argv

    try:
        program_name = argv[0]
        parser = SmokeTestArgumentParser(prog=program_name)
        args = parser.parse_args(argv[1:])

        suite(args)

    except SystemExit as exc:
        exit_status = exc.code

    return exit_status


if __name__ == "__main__":
    exit_status = main(sys.argv)
    sys.exit(exit_status)


# Copyright © 2016–2023 Ben Finney <bignose@debian.org>
#
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 3 of that license or any later version.
# No warranty expressed or implied.


# Local variables:
# coding: utf-8
# mode: python
# End:
# vim: fileencoding=utf-8 filetype=python :
