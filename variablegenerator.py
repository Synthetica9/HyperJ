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

class VariableGenerator(object):
    def __init__(self, defaultvariable=None):
        self.variables = dict()
        self.defaultvariable=defaultvariable
        self.n = 0

    def __getitem__(self, name):
        if name.startswith('@'):  # Specifying a new variable:
            name = name[1:]
            # Remove the starting '@'

            currentvalue = self.variables.get(name, 0) + 1
            # using get, in case it is not defined

            self.variables[name] = currentvalue
            # Now it is either 1 or its old value + 1
        else:
            currentvalue = self.variables[name]

        return '{name}_{currentvalue}'.format(**locals())

    def next(self):
        if self.defaultvariable is not None:
            self.n += 1
            return '{varname}_{n}'.format(
                varname=self.defaultvariable,
                n=self.n
            )
        else:
            raise TypeError()