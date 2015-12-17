# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/Argument.py

"""Contains the implementation for Argument(object)."""

from .Exceptions import Error

class Argument(object):
    """
    An abstract base class for derived argument types used by CLI.
    """
    def __init__(self, description, default=None, short=None, name=None):
        """A *description* is required of **all** Arguments.
        A *default* value is required for a Default, Switch, or Flag.

        description: str
            A short description of the Argument to be displayed with the
            *help* Flag is given.

        default: ...
            The *value* the Argument should take if it is not provided at
            the command line. When given the *dtype* member will become
            `type(default)`.

        short: str
            The single character alternate name for the Argument. For Flags
            these can be stacked together (e.g., -abc).

        name: str
            When not given, the *name* member will be assigned later from
            the variable name itself. If you wish to overide this implicit
            behavior, specify an alternative name here.
        """

        self.description = str(description)
        self.default     = default
        self.dtype       = type(default)
        self.short       = None if not short else str(short)
        self.value       = self.default
        self.given       = False
        self.name        = None if not name else str(name)


    def set(self, value):
        """Set the value of the Argument; coerce into self.dtype."""
        self.value = self.dtype(value)


    def help(self, spacing=10):
        """The *help* method **must** be implemented by derived Arguments!"""
        raise Error("The *help* method was not implemented for {}".format(type(self)))


    def __str__(self):
        """Return a string representation of the object."""
        return ("{}{}\n{}\nvalue={}{}".format(
                "" if not self.name else "{}: ".format(self.name), self.dtype,
                self.description, self.value,
                "" if not self.short else ", short={}".format(self.short)))


    def __repr__(self):
        """Return a string representation of the object."""
        return str(self)
