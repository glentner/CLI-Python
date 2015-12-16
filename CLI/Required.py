# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/Required.py

"""Implementation of Required(Argument)."""

from .Argument import Argument

class Required(Argument):
    """A Required *Argument* is one with no *default* value."""


    def __init__(self, description, dtype=str):
        """Initialize the new Required(Argument)."""
        super(Required, self).__init__(description)
        self.dtype = dtype


    def help(self, spacing = 10):
        """Return a the *help* string for this *Argument*."""
        return " {}{}{} (required).\n".format(self.name, " " * (spacing -
                                              len(self.name)), self.description)
