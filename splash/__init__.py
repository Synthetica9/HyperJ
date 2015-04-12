__author__ = 'Synthetica'
import tools
from random import choice

print tools.module_path()

def splash(ret=False, **flags):
    # f=tools.load_resource('splash/quotes.txt')
    with tools.load_resource('splash/quotes.txt') as f:
        string = "\n".join([r" _    _                           _  ",
                            r"| |  | |                         | | ",
                            r"| |__| |_   _ _ __   ___ _ __    | | ",
                            r"|  __  | | | | '_ \ / _ \ '__|   | | ",
                            r"| |  | | |_| | |_) |  __/ | | |__| | ",
                            r"|_|  |_|\__, | .__/ \___|_|  \____/  ",
                            r"         __/ | |{version}",
                             "        |___/|_|{status}\n"]).format(
            version=flags.get('version', '0.0.0').rjust(19),
            status=choice(f.readlines()).strip().rjust(19))
    if ret:
        return string
    else:
        print string