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
import splash


def interactive_console(*functions, **flags):
    if not flags.get('nosplash', False):
        splash.splash(**flags)

    else:
        banner = 'HyperJ {}'.format(flags.get('version', '0.0.0'))
        print banner
        print len(banner) * '='
        # Boring.

    while True:
        print '0)\t Exit'
        print '1)\t Setup flags'
        for i, j in enumerate(functions):
            print '{n})\t {name}'.format(n=i+2, name=j.__name__)
        try:
            c = int(raw_input('??) '))
        except ValueError:
            print "!!)\t Incorrect value!"
            break
        if c == 0:
            print "!!)\t Bye!"
            exit(0)
        elif c == 1:
            print "!?)\t Change what flag?"
            flag = raw_input('??) ')
            print "!?)\t To what?"
            value = input('??) ')
            # Someone who you don't trust should not have access to  this
            # console at any rate, so the use of input() here should be fine.
            flags[flag] = value
        else:
            if c >= 2:
                c -= 2
            f = functions[c]
            print "!!)\t Interacting with {f}".format(f=f)
            while True:
                string = raw_input('#!) ')
                print f(string, **flags)

def main(**flags):
    import lexer

    interactive_console(
        lexer.lexer,
        **flags
    )


if __name__ == '__main__':
    main()