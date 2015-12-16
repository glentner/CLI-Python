# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/List.py

"""Implementation of List(Argument)."""

from .Argument import Argument

class List(Argument):
    """A List *Argument* is similar to a Required(Argument), with the important
    distiction that it will take an arbitrary number of values from the command
    line.
    """

    def __init__(self, description, dtype=str):
        """Initialize the new List(Argument)."""
        super(List, self).__init__(description)
        self.dtype = dtype


    def help(self, spacing = 10):
        """Return a the *help* string for this *Argument*."""
        return " {}...{}{} (required).\n".format(self.name, " " * (spacing - len(self.name) - 3),
                self.description)


    def set(self, value):
        """Specialization for List argument."""
        self.value = [ self.dtype(v) for v in value ]
