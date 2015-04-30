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

import collections
import string
import itertools
import json
import re

import lexer
import tools
from variablegenerator import VariableGenerator

builtins_dict = json.load(tools.load_resource('items.json'))


def build_pattern(fle, **flags):
    debug = flags['debug']
    lines = fle.readlines()

    # First, we filter out new lines:
    lines = (line.strip('\n') for line in lines)
    # Then, we filter out comments:
    lines = (line[:line.index('#')] if '#' in line else line for line in lines)
    # Next, we filter out all the empty lines that remain after this process.
    lines = [line for line in lines if line]

    if debug >= 5:
        print 'Lines from pattern:'
        print lines
        print

    patterns = collections.OrderedDict()
    for line in lines:
        if not any(line.startswith(char) for char in string.whitespace):
            patterns[line] = collections.OrderedDict()
            current_key = line
        else:
            key, value = line.strip().split(':', 1)
            key = key.strip()
            value = value.strip()
            patterns[current_key][key] = value

    if debug >= 5:
        print 'pattern:'
        print {a: dict(b) for a, b in patterns.iteritems()}
        print '(Note: this is not guaranteed to be in the right order)'
        print

    return patterns

def match(pattern, to_match):
    returnvalue = True
    for i, j in itertools.izip_longest(pattern.split(), to_match,
                                       fillvalue=''):
        print repr(i), ':', repr(j), ':', match_single(i, j)
        if not match_single(i, j):
            returnvalue = False

    return returnvalue

def match_single(pattern, to_match):
    if '|' in pattern:
        return any(match_single(sub_pattern, to_match)
                   for sub_pattern in pattern.split('|'))
    elif pattern.startswith('!'):
        return not match_single(pattern[1:], to_match)
        # Remove ! and try again
    elif pattern == '?':
        return True  # Always matches
    else:
        if match_type(pattern, to_match):
            return True

#TODO: Bad globals
typedict = {}

def match_type(tpe, item):

    if tpe == 'edge':
        return item is None

    if isinstance(item, basestring):
        regular_match = any(re.match(pattern, item)
                            for pattern_type, pattern in regexes
                            if pattern_type == tpe)
        if regular_match:
            return True

    if item in builtins_dict:
        return tpe == builtins_dict[item]['type']

    if item in typedict:
        return tpe == typedict[item]

    return False

def single_op(lexed, **flags):
    debug = flags['debug']
    generator = VariableGenerator()
    formatter = string.Formatter()
    output = []
    global regexes  # TODO: bad practice, remove later.
    regexes = list(lexer.build_regex(**flags))
    if debug >= 5:
        print 'regexes:'
        print regexes
        print
    fle = tools.load_resource('semi_assembly_generator/patterns.ptrn')
    patterns = build_pattern(fle, **flags)
    for line in lexed:
        line = [None] + line + [None]
        index_last = index_first = -1
        while len(line) > 3:
            for pattern, consequence in patterns.iteritems():
                to_match = line[index_first:index_last]
                matched = match(pattern, to_match)
                print pattern, to_match, matched
                print
                if matched:
                    for kind, action in consequence.iteritems():
                        print kind, ':', action
                        if kind == 'output':
                            output.append(
                                formatter.vformat(action, to_match, generator)
                            )
                        if kind == 'replace':
                            replacement = formatter.vformat(
                                action,
                                to_match + [''],
                                # Fix for ? at the end of a line matching
                                # nothing (Intended behavior, but slightly
                                # annoying in this case)
                                generator).split()
                            line = line[:index_first] + replacement + line[index_last:]
                            if debug >= 6:
                                print 'New line: '
                                print line
                                print
                        if kind == 'type':
                            to_handle = formatter.vformat(
                                action,
                                to_match,
                                generator
                            )
                            key, value = to_handle.split(' ')
                            typedict[key] = value

                    index_last = index_first = -1
                    break


            else:
                index_first -= 1
                index_last = min(-1, index_first+4)
    return output


# http://jsoftware.com/help/jforc/parsing_and_execution_ii.htm
# # TODO: account for monad literals
#
#
# import json
# import operator
# import re
# import itertools
#
# import tools
# import variablegenerator
# import lexer
# from errors import ParserException
#
#
# def match_pattern(pattern, item):
#     try:
#         return all(any(a == j for a in i) or i == j
#                    for i, j in
#                    itertools.izip_longest(pattern, item, fillvalue=None))
#     except TypeError:
#         return False
#
#
# def single_op(lexed, **flags):
#     debug = flags['debug']
#     regexes = list(lexer.build_regex(**flags))
#     anonymous = variablegenerator.VariableGenerator('anonymous')
#     storage = variablegenerator.VariableGenerator('tmp_storage')
#     literal = variablegenerator.VariableGenerator('literal')
#     storage = variablegenerator.VariableGenerator('tmp_storage')
#     usedtokens = reduce(operator.__or__, map(set, lexed))
#     # usedtokens now contains all different tokens used in the source code
#     if debug >= 5:
#         print 'Tokens used in source:'
#         print usedtokens
#         print
#     debug = flags['debug']
#     with tools.load_resource('items.json') as opfile:
#         oplist = json.load(opfile)
#     if debug >= 8:
#         print 'Oplist:'
#         print oplist
#         print
#     types = dict()
#     result = []
#     for line in lexed:
#         context = None
#         line = [None] + line  # Add an edge marker
#         currenttokens = []
#         currenttypes = []
#         if debug >= 7:
#             print "Simplifying line:"
#             print line
#             print
#         while line:
#             currenttoken = line.pop()
#             assert isinstance(currenttoken, basestring) or currenttoken is None
#             # Can be unicode or str.
#             currenttokens = [currenttoken] + currenttokens
#             if isinstance(currenttoken, basestring):
#                 possible_types = []
#                 for typename, regex in regexes:
#                     if re.match(regex, currenttoken):
#                         possible_types.append(typename)
#                 current_type = possible_types[0]
#                 if current_type == 'name':
#                     if currenttoken in types:
#                         current_type = 'name_' + types[currenttoken]
#
#                 elif current_type == 'item':
#                     if currenttoken not in oplist:
#                         raise ParserException('Unknow token', currenttoken)
#                         # Unknown token
#                     current_type = oplist[currenttoken]['type']
#             elif currenttoken is None:
#                 current_type = 'edge'
#             currenttypes = [current_type] + currenttypes
#             if debug >= 7:
#                 print 'Current tokens:'
#                 print currenttokens
#                 print 'Current types:'
#                 print currenttypes
#                 print
#
#             # assign literal to name
#             if current_type == 'noun':
#                 tmp_name = literal.next()
#                 result.append('ASSIGN LITERAL {name} {literal}'.format(
#                     name=tmp_name,
#                     literal=currenttoken
#                 ))
#                 currenttoken = tmp_name
#                 current_type = 'name_noun'
#                 currenttypes[-1] = current_type
#                 currenttokens[-1] = currenttoken
#                 types[tmp_name] = 'noun'
#
#             if currenttypes == ['edge']:
#                 if context is not None:
#                     result.append('END')
#                 break
#
#             elif current_type in ['directive', 'comment']:
#                 currenttypes.pop()
#                 currenttokens.pop()
#                 if current_type == 'directive':
#                     context = currenttoken[3:].strip()
#                     result.append('CONTEXT {context}'.format(
#                         context=context
#                     ))
#
#
#             # Pattern: noun assign
#             elif match_pattern([['edge'],
#                                 ['name', 'name_noun'],
#                                 ['assign'],
#                                 ['name_noun', 'noun']],
#                                currenttypes):
#                 result.append('ASSIGN {location} {name} {item}'.format(
#                     location='GLOBAL' if currenttokens[2] == '=:' else 'LOCAL',
#                     name=currenttokens[1],
#                     item=currenttokens[3]
#                 ))
#                 types[currenttokens[1]] = 'noun'
#                 for i in range(3):  # remove last 2 items, leave the name:
#                     currenttypes.pop()
#                     currenttokens.pop()
#
#
#
#             # Pattern: dyad apply
#             elif match_pattern([['noun', 'name_noun'],
#                                 ['verb', 'name_verb'],
#                                 ['noun', 'name_noun']],
#                                currenttypes):
#                 tmp_name = storage.next()
#                 result.append('APPLY DYAD {verb} {right} {left} {storage}'.format(
#                     verb=currenttokens[1],
#                     right=currenttokens[0],
#                     left=currenttokens[2],
#                     storage=tmp_name
#                 ))
#                 for i in range(3):  # remove last 2 items, leave the name:
#                     currenttypes.pop()
#                     currenttokens.pop()
#
#                 line.append(tmp_name)
#
#             # Pattern: monad apply
#             elif match_pattern([['verb', 'name_verb'],
#                                 ['noun', 'name_noun']],
#                                currenttypes[1:]):
#                 tmp_name = storage.next()
#                 result.append('APPLY MONAD {verb} {right} {storage}'.format(
#                     verb=currenttokens[1],
#                     right=currenttokens[2],
#                     storage=tmp_name
#                 ))
#
#                 types[tmp_name] = 'noun'
#                 line.append(currenttokens[0])
#                 line.append(tmp_name)
#
#                 for i in range(3):  # remove last 2 items, leave the name:
#                     currenttypes.pop()
#                     currenttokens.pop()
#
#                 # currenttypes.append('name_noun')
#                 # currenttokens.append(tmp_name)
#
#                 # if currenttypes[0] == 'edge':
#                 #     result.append('SHOW {storage}'.format(
#                 #         storage=tmp_name
#                 #     ))
#
#             # Pattern: show result
#             elif match_pattern([['edge'],
#                                 ['noun', 'name_noun']],
#                                currenttypes):
#                 result.append('SHOW {item}'.format(
#                     item=currenttokens[1]
#                 ))
#
#         if context is not None:
#             if not result[-1].startswith('CONTEXT'):
#                 result.append('ENDCONTEXT')
#                 context = None
#             else:
#                 result.pop()
#
#     return result