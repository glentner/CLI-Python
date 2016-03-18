# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/Default.py

"""Implementation of Default(Argument)."""

from .Argument import Argument

class Default(Argument):
    """
    A Default *Argument* is one with a *default* value and does
    not necessarily need to be provided.
    """

    def __init__(self, description, default, name=None):
        """Initialize the new Default(Argument)."""
        super(Default, self).__init__(description, default, name=name)


    def help(self, spacing = 10):
        """Return a the *help* string for this *Argument*."""
        return " {}{}{} (default: {}).\n".format(self.name, " " * (spacing - len(self.name)),
                                                 self.description, self.default)
