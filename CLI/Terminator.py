# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/Terminator.py

"""Implementation of Terminator(Argument)."""

from .Argument   import Argument
from .Exceptions import Error

class Terminator(Argument):
    """
    A Terminator *Argument* is a Flag that will stop the execution
    but display some requested information about the program (e.g.,
    --copyright).
    """

    def __init__(self, description, information, short=None):
        """Initialize the new Terminator(Argument)."""
        super(Terminator, self).__init__(description, False, short)
        self.information = information


    def help(self, spacing = 10):
        """Return the *help* string for this *Argument*."""
        if not self.short:
            return " --{}{}{} (default: {}).\n".format(self.name, " " *
                    (spacing - len(self.name) - 2), self.description, self.default)
        else:
            return " -{}, --{}{}{} (default: {}).\n".format(self.short, self.name,
                    " " * (spacing - len(self.name) - 6), self.description, self.default)


    def set(self, value):
        """Specialized method for setting the *value* of the Flag."""
        if type(value) is bool:
            self.value = value
        elif type(value) is str:
            if value.strip() not in ["0", "1"]:
                raise Error("The Flag(Argument) `{}`: can only take '0' or '1'!".format(self.name))
        else:
            # the behavior is dictated by coercion (be careful!)
            self.value = bool(value)
