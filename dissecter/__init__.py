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
from errors import ParserException
import variablegenerator

__author__ = 'Synthetica'

import tools

def single_assignment(lexed, **flags):
    debug = flags['debug']
    result = []
    for line in lexed:
        while ('=.' in line) or ('=:' in line):
            try:
                global_index = tools.rindex(line, '=:')
            except ValueError:
                global_index = -1

            try:
                local_index = tools.rindex(line, '=.')
            except ValueError:
                local_index = -1

            assignment_index = max(global_index, local_index)
            if assignment_index == -1:
                raise ValueError()

            if assignment_index == 1:  # Second item
                break

            result.append(line[assignment_index-1:])
            line = line[:assignment_index]
        result.append(line if '=.' in line or '=:' in line
                      else ['print.']+line)
    return result


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


def parser(lexed, **flags):
    lexed = solve_parrens(lexed, **flags)
    lexed = single_assignment(lexed, **flags)
    return lexed