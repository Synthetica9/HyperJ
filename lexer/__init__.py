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
import re
import string

from errors import LexerException
# TODO: neater input of regular_chars (hardcoded?)
# TODO: all things as character groups (more compact regexes)
# TODO: Comments
# TODO: @.: directive statements
# TODO: Enhanced comments

def build_regex(enhanced_parsing=True, debug=0, **flags):
    re_flags = (re.DEBUG if debug >= 6 else 0)

    # letters = string.ascii_letters
    letters = '[A-Za-z]'
    # digits = string.digits + '_'
    digits = '[0-9_]'
    whitespace = '[ \t]'
    # Not very portable, but better than taking string.whitespace and manually
    # removing everything that we don't want.

    if enhanced_parsing:
        non_sticking_tokens = "['()]"
        # Signals (: and ): as a special case, with 2 separate tokens.
    else:
        non_sticking_tokens = "[']"  # "'':" has ["''", ':'] as result.
    sticking_chars = '[:\.]'

    regular_chars = '[{}]'.format(
        re.escape(
            ''.join(char for char in string.punctuation
                    if not re.match(
                        non_sticking_tokens,
                        char
                    )
            )
        )
    )
    if debug >= 3:
        print 'Regular chars:'
        print regular_chars
        print

    re_names = ('{letters}'
                # A name has to start with a letter (no underscores allowed)
                '(?:{letters}|{digits})*'
                # Next, any digit or letter can follow.
                '(?!{sticking_chars}|{letters}|{digits})'
                # This negative lookbehind makes sure we catch the entire word,
                # and that the word doesn't end in . or :.
                ).format(**locals())

    if debug >= 3:
        print 'Regex for names:'
        print re_names
        re.compile(re_names, re_flags)
        print

    re_string = ("'"
                 # Opening quote
                 "(?:[^']|'')*"
                 # non-capturing group of an unlimited amount of characters and
                 # double quotes
                 "'"
                 # Closing quote
                 )

    if debug >= 3:
        print 'Regex for strings:'
        print re_string
        re.compile(re_string, re_flags)
        print

    re_single_number = ('(?:'
                        # Start a non-capturing group
                        '{digits}'
                        # First character has to be a digit
                        '(?:{digits}|{letters}|\.)*'
                        # after that, any combination of numbers, letters and
                        # dots can follow
                        ')'
                        ).format(**locals())

    if debug >= 3:
        print 'Regex for single numbers:'
        print re_single_number
        re.compile(re_single_number, re_flags)
        print

    re_number_group = ('(?<!{letters}|{digits})'
                       '(?:'
                       '{re_single_number}'
                       '{whitespace}+'
                       ')*'
                       '{re_single_number}'
                       '(?!{letters}|{digits}|{sticking_chars})'
                       ).format(**locals())
    if debug >= 3:
        print 'Regex for number groups:'
        print re_number_group
        re.compile(re_number_group, re_flags)
        print

    re_regular_items = ('{regular_chars}'
                        '{sticking_chars}*'
                        ).format(**locals())

    if debug >= 3:
        print 'Regex for regular items:'
        print re_regular_items
        re.compile(re_regular_items, re_flags)
        print

    re_alphanumeric_items = ('(?:'
                             '{digits}|{letters}'
                             ')+'
                             '{sticking_chars}+'
                             ).format(**locals())
    if debug >= 3:
        print 'Regex for alphanumeric items:'
        print re_alphanumeric_items
        re.compile(re_alphanumeric_items, re_flags)
        print

    re_comment = (r'NB\.'
                  r'.*')
    # If NB. is encountered, eat everything until eol.
    if debug >= 3:
        print 'Regex for comments:'
        print re_comment
        re.compile(re_comment, re_flags)
        print

    re_directive = r'@\.:[^)]*'
    # When encountering an directive statement (that's what they are called for
    # now), eat everything until the next close paren (that is totally allowed
    # to never come)


    if debug >= 3:
        print 'Regex for directive statements:'
        print re_directive
        re.compile(re_directive, re_flags)
        print

    return (
        re_names,
        re_directive,
        re_number_group,
        re_alphanumeric_items,
        re_string,
        re_comment,
        re_directive,
        re_regular_items
        # The order here is important.
    )

def lexer(code, debug=0, **flags):
    regexes = build_regex(debug=debug, **flags)
    # This might seem wasteful, but it does allow for the rebuilding of the
    # regex with different flags.
    if debug >= 2:
        print 'Using following regex to parse:'
        for regex in regexes:
            print regex
        print

    returnlist = []
    for line in code.splitlines():
        tmpreturn = []
        if debug >= 7:
            print 'Parsing the following line:'
            print line
            print
        if line.count("'") % 2 != 0:
            # unclosed quotes. Always (except with comments):
            raise LexerException('Unclosed quote!')
        while line:
            line = line.strip()
            for regex in regexes:
                match = re.match(regex, line)
                if match:
                    tmpreturn.append(match.group())
                    line = line[match.end():]
                    break

            else:
                raise LexerException('Unknown token')
        returnlist.append(tmpreturn)
        if debug >= 7:
            print 'Line parsed to:'
            print tmpreturn
            print

    return returnlist


if __name__ == '__main__':
    while 1:
        print lexer(raw_input('>>> '), debug=7)
