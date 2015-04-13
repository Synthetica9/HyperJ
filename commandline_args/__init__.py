# Copyright 2015 Patrick Hilhorst
#
# This file is part of HyperJ.
#
# HyperJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HyperJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HyperJ.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Synthetica'

import argparse

parser = argparse.ArgumentParser(description='HyperJ compiler',
                                 fromfile_prefix_chars='@')
parser.add_argument('infile', nargs='?',
                    help='Specify the filename to be used. No filename means '
                         'that a console will be opened.')
parser.add_argument('outfile', nargs='?',
                    help='Specify the output filename. Defaults to the input '
                         'filename with .out appended (a.hjs -> a.hjs.out). '
                         'Can also be stdout.')
parser.add_argument('--debug', '-d', metavar='L', type=int, default=0,
                    help='Set the debug level, on a scale from 0 to 10. '
                         'A higher number means more (potentially useless) '
                         'output. Defaults to 0, meaning there will not be '
                         'any debug output. This will not change the code'
                         'output, only the output on stdout.')
parser.add_argument('--standard-parsing', action='store_false',
                    dest='enhanced-parsing',
                    help='Use a parser closer to J\'s standard parser; '
                         'disabling a few useful HyperJ parsing tweaks.')
parser.add_argument('--nosplash', action='store_true',
                    help='Disable the splashscreen, and show a boring initial '
                         'message.')

if __name__ == '__main__':
    args = parser.parse_args()
    print repr(args)