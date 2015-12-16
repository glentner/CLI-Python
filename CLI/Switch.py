# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/Switch.py

"""Implementation of Switch(Argument)."""

from .Argument import Argument

class Switch(Argument):
    """
    A Switch *Argument* is one with a *default* value and does
    not necessarily need to be provided. The value to be assigned
    **must** follow the flag on the command line.
    """


    def __init__(self, description, default, short=None):
        """Initialize the new Switch(Argument)."""
        super(Switch, self).__init__(description, default, short)


    def help(self, spacing = 10):
        """Return the *help* string for this *Argument*."""
        if not self.short:
            return " --{}{}{} (default: {}).\n".format(self.name, " " *
                    (spacing - len(self.name) - 2), self.description, self.default)
        else:
            return " -{}, --{}{}{} (default: {}).\n".format(self.short, self.name,
                    " " * (spacing - len(self.name) - 4), self.description, self.default)
