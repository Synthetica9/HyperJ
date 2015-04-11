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
from random import choice

def interactive_console(*functions, **flags):
    if not flags.get('nosplash', False):
        with open('quotes.txt') as f:
            print "\n".join([r" _    _                           _    ",
                             r"| |  | |                         | |   ",
                             r"| |__| |_   _ _ __   ___ _ __    | |   ",
                             r"|  __  | | | | '_ \ / _ \ '__|   | |   ",
                             r"| |  | | |_| | |_) |  __/ | | |__| |   ",
                             r"|_|  |_|\__, | .__/ \___|_|  \____/    ",
                             r"         __/ | |              {version}",
                             r"        |___/|_| {status}"]
                            ).format(version=flags.get('version', '0.0.0'),
                                     status=choice(f.readlines()))

    else:
        print 'HyperJ'
        print '======='
        #Boring.

    while True:
        print '0)\t Exit'
        print '1)\t Setup flags'
        for i, j in enumerate(functions):
            print '{n}\t {name}'.format(n=i+2, name=j.__name__)
        c = raw_input('??) ')


def main(**flags):
    import lexer
    interactive_console(
        lexer.lexer,
        **flags
    )

if __name__=='__main__':
    main()