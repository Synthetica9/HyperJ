__author__ = 'Synthetica'
import tools
import json

def single_op(lexed, **flags):
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
        if debug >= 7:
            print "Simplifying line:"
            print line
            print
    return lexed