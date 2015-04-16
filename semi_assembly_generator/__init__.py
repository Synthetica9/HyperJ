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

# http://jsoftware.com/help/jforc/parsing_and_execution_ii.htm
# TODO: account for monad literals

import json
import operator
import re
import itertools

import tools
import variablegenerator
import lexer
from errors import ParserException


def match_pattern(pattern, item):
    try:
        return all(any(a == j for a in i) or i == j
                   for i, j in
                   itertools.izip_longest(pattern, item, fillvalue=None))
    except TypeError:
        return False


def single_op(lexed, **flags):
    debug = flags['debug']
    regexes = list(lexer.build_regex(**flags))
    anonymous = variablegenerator.VariableGenerator('anonymous')
    storage = variablegenerator.VariableGenerator('tmp_storage')
    literal = variablegenerator.VariableGenerator('literal')
    storage = variablegenerator.VariableGenerator('tmp_storage')
    usedtokens = reduce(operator.__or__, map(set, lexed))
    # usedtokens now contains all different tokens used in the source code
    if debug >= 5:
        print 'Tokens used in source:'
        print usedtokens
        print
    debug = flags['debug']
    with tools.load_resource('items.json') as opfile:
        oplist = json.load(opfile)
    if debug >= 8:
        print 'Oplist:'
        print oplist
        print
    types = dict()
    result = []
    for line in lexed:
        line = [None] + line  # Add an edge marker
        currenttokens = []
        currenttypes = []
        if debug >= 7:
            print "Simplifying line:"
            print line
            print
        while line:
            currenttoken = line.pop()
            assert isinstance(currenttoken, basestring) or currenttoken is None
            # Can be unicode or str.
            currenttokens = [currenttoken] + currenttokens
            if isinstance(currenttoken, basestring):
                possible_types = []
                for typename, regex in regexes:
                    if re.match(regex, currenttoken):
                        possible_types.append(typename)
                current_type = possible_types[0]
                if current_type == 'name':
                    if currenttoken in types:
                        current_type = 'name_' + types[currenttoken]

                elif current_type == 'item':
                    if currenttoken not in oplist:
                        raise ParserException('Unknow token', currenttoken)
                        # Unknown token
                    current_type = oplist[currenttoken]['type']
            elif currenttoken is None:
                current_type = 'edge'
            currenttypes = [current_type] + currenttypes
            if debug >= 7:
                print 'Current tokens:'
                print currenttokens
                print 'Current types:'
                print currenttypes
                print

            # assign literal to name
            if current_type == 'noun':
                tmp_name = literal.next()
                result.append('ASSIGN LITERAL {name} {literal}'.format(
                    name=tmp_name,
                    literal=currenttoken
                ))
                currenttoken = tmp_name
                current_type = 'name_noun'
                currenttypes[-1] = current_type
                currenttokens[-1] = currenttoken
                types[tmp_name] = 'noun'

            if currenttypes == ['edge']:
                break
            # Pattern: noun assign
            elif match_pattern([['name', 'name_noun'],
                                ['assign'],
                                ['name_noun', 'noun']],
                               currenttypes):
                result.append('ASSIGN {location} {name} {item}'.format(
                    location='GLOBAL' if currenttokens[1] == '=:' else 'LOCAL',
                    name=currenttokens[0],
                    item=currenttokens[2]
                ))
                for i in range(2):  # remove last 2 items, leave the name:
                    currenttypes.pop()
                    currenttokens.pop()

                types[currenttoken[-1]] = 'noun'

            # Pattern: dyad apply
            elif match_pattern([['noun', 'name_noun'],
                                ['verb', 'name_verb'],
                                ['noun', 'name_noun']],
                               currenttypes):
                tmp_name = storage.next()
                result.append('APPLY DYAD {verb} {right} {left} {storage}'.format(
                    verb=currenttokens[1],
                    right=currenttokens[0],
                    left=currenttokens[2],
                    storage=tmp_name
                ))
                for i in range(3):  # remove last 2 items, leave the name:
                    currenttypes.pop()
                    currenttokens.pop()

                currenttypes.append('name_noun')
                currenttokens.append(tmp_name)

            # Pattern: monad apply
            elif match_pattern([['verb', 'name_verb'],
                                ['noun', 'name_noun']],
                               currenttypes[1:]):
                tmp_name = storage.next()
                result.append('APPLY MONAD {verb} {right} {storage}'.format(
                    verb=currenttokens[0],
                    right=currenttokens[1],
                    storage=tmp_name
                ))
                for i in range(2):  # remove last 2 items, leave the name:
                    currenttypes.pop()
                    currenttokens.pop()

                currenttypes.append('name_noun')
                currenttokens.append(tmp_name)

    return result