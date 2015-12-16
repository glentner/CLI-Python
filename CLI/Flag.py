# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/Flag.py

"""Implementation of Flag(Argument)."""

from .Argument   import Argument
from .Exceptions import Error

class Flag(Argument):
    """
    A Flag *Argument* is a Switch that assumes True/False. No
    value should follow a Flag. Flags may be *stacked* by their
    *short* name (e.g., -abc).
    """

    def __init__(self, description, default, short=None):
        """Initialize the new Flag(Argument)."""
        super(Flag, self).__init__(description, default, short)


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
