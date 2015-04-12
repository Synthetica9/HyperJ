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

# This is the main file of HyperJ, and the thing that you will likely be
# executing.
import sys

def main():
    import commandline_args
    args = commandline_args.parser.parse_args()
    flags = args.__dict__
    if args.debug >= 7:
        print 'Arguments namespace: '
        print repr(args)
    if args.infile is None:
        import console
        console.main(**flags)
    else:
        import lexer
        raw_code = open(args.infile).read()
        lexed = lexer.lexer(raw_code, **flags)

        import dissecter
        solved = dissecter.parser(lexed, **flags)
        if args.outfile == 'stdout':
            outfile = sys.stdout
        else:
            if args.outfile is None:
                args.outfile = args.infile + '.out'
            outfile = open(args.outfile, 'w')
        outfile.write('\n'.join(map(str, solved)))
        # TODO: make sure the names here don't overlap
        # There are 2 conceivable solutions for this:
        # 1. change the names of the input, by adding a prefix
        # 2. different notation for 'system variables'
        # 1 seems the more reasonable approach.


if __name__ == '__main__':
    main()