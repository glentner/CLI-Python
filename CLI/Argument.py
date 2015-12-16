# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/Argument.py

"""Contains the implementation for Argument(object)."""

from .Exceptions import Error

class Argument(object):
    """
    An abstract base class for derived argument types used by CLI.
    """
    def __init__(self, description, default=None, short=None):
        """A *description* are required of **all** Arguments.
        A *default* value is required for a Default, Switch, or Flag.
        """
        self.description = str(description)
        self.default     = default
        self.dtype       = type(default)
        self.short       = None if not short else str(short)

        self.value = self.default
        self.given = False


    def set(self, value):
        """Set the value of the Argument; coerce into self.dtype."""
        self.value = self.dtype(value)


    def help(self, spacing=10):
        """The *help* method **must** be implemented by derived Arguments!"""
        raise Error("The *help* method was not implemented for {}".format(type(self)))


    def __str__(self):
        """Return a string representation of the object."""
        return ("{}\n".format(type(self)) +
                "{}\n".format(self.description) +
                "value={}, dtype={}".format(self.value, self.dtype) +
                "\n" if not self.short else ", short={}\n".format(self.short))


    def __repr__(self):
        """Return a string representation of the object."""
        return str(self)
