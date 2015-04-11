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

    # regular_chars = re.escape(
    # ''.join(  # TODO: string.printable is derived from string.punctuation.
    # set(string.punctuation)
    # - set(non_sticking_tokens)
    # - set(sticking_chars)
    #     )
    # )

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

    re_comment = ('NB.'
                  '.*')

    # If NB. is encountered, eat everything until eol.
    #
    # return '|'.join('({})'.format(item)
    #                 for item in (
    #     re_names,
    #     re_number_group,
    #     re_alphanumeric_items,
    #     re_regular_items,
    #     re_string
    # ))
    return '|'.join((
        re_names,
        re_number_group,
        re_alphanumeric_items,
        re_regular_items,
        re_string,
        re_comment
    ))

def lexer(code, debug=0, **flags):
    regex = build_regex(**flags)
    if debug >= 2:
        print 'Using following regex to parse:'
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
            match = re.match(regex, line)
            if match:
                tmpreturn.append(match.group())
                line = line[match.end():]
            else:
                raise LexerException
        returnlist.append(tmpreturn)
        if debug >= 7:
            print 'Line parsed to:'
            print tmpreturn
            print

    return returnlist



if __name__ == '__main__':
    while 1:
        print lexer(raw_input('>>> '), debug=7)
