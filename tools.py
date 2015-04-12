__author__ = 'Synthetica'
import sys
import os

# Source: http://stackoverflow.com/a/2632297/2872678
def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))

def load_resource(relative_path, *args, **kwargs):
    mainpath = module_path()
    resource_path = os.path.normcase(relative_path)
    return open(os.path.join(mainpath, resource_path), *args, **kwargs)

# Source: http://stackoverflow.com/a/9836903/2872678
def rindex(lst, item):
    """
    Find first place item occurs in any item, but starting at end of list.
    Return index of item in list, or -1 if item not found in the list.
    """
    i_max = len(lst)
    i_limit = -i_max
    i = -1
    while i >= i_limit:
        if lst[i] == item:
            return i_max + i
        i -= 1
    raise ValueError()