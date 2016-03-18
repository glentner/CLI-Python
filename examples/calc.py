#!/usr/bin/env python3
# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# examples/calc.py

"""calc.py

An example program to showcase the CLI.MultiMode API.
"""

import sys, CLI

class Operator(CLI.SingleMode):
    """Generic operation class for Calc."""

    def __init__(self, argv):
        """Define to operands `a` and `b`."""

        super(Operator, self).__init__(argv)

        self.a = CLI.Required("LHS operator", dtype=float)
        self.b = CLI.Required("RHS operator", dtype=float)

    def main(self):
        """Operator `a` on `b`."""

        print("result: {}".format(self.operate()))
        return 0

    def operate(self):
        """Must be implemented by derived class!"""
        raise NotImplemented("The operate() method has not been implemented for "
                "{}.".format(type(self)))


class Add(Operator):
    """An addition Operator."""
    def operate(self):
        return self.a + self.b

class Sub(Operator):
    """A subtraction Operator."""
    def operate(self):
        return self.a - self.b

class Mul(Operator):
    """A multiplcation Operator."""
    def operate(self):
        return self.a * self.b

class Div(Operator):
    """A division Operator."""
    def operate(self):
        return self.a / self.b


class Calc(CLI.MultiMode):
    """A simple calculator application to showcase the CLI.MultiMode API. Pass the -h | --help
    flag for more information, or one of the subcommands likewise.
    """

    def __init__(self, argv):

        super(Calc, self).__init__(argv)

        self.SubCommands['add'] = Add
        self.SubCommands['sub'] = Sub
        self.SubCommands['mul'] = Mul
        self.SubCommands['div'] = Div


if __name__ == '__main__':
    sys.exit( Calc(sys.argv).Exe() )
