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

import tools
import variablegenerator
from errors import ParserException

def solve_parrens(lexed, **flags):
    debug = flags['debug']
    generator = variablegenerator.VariableGenerator('parentheses')
    result = []
    for line in lexed:
        if debug >= 6:
            print 'Removing parrens from:'
            print line
            print

        while '(' in line:
            if line.count('(') != line.count(')'):
                raise ParserException()
                # Here be unmatched parrens.
            last_open_parren = tools.rindex(line, '(')
            #    x=:1
            #    (x=:>:x),(x=:>:x),(x=:>:x)
            # 4 3 2
            # This is how it works; last brackets are eval'ed last.
            matching_close_parren = (line[last_open_parren:].index(')')
                                     + last_open_parren)
            contents = line[last_open_parren+1:matching_close_parren]
            varname = generator.next()
            prevline = [varname, '=.'] + contents
            if debug >= 6:
                print 'parren contents:'
                print prevline
                print
            result.append(prevline)
            line = (line[:last_open_parren] +
                    [varname] +
                    line[1+matching_close_parren:])
            if debug >= 7:
                print 'Line is now:'
                print line
                print
        result.append(line)
    return result

if __name__ == '__main__':
    print solve_parrens([['a', '(', 'b', ')', 'c']], debug=10)