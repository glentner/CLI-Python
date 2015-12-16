# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/Terminator.py

"""Implementation of Terminator(Argument)."""

from .Argument import Argument

class Terminator(Argument):
    """
    A Terminator *Argument* is a Flag that will stop the execution
    but display some requested information about the program (e.g.,
    --copyright).
    """

    def __init__(self, description, information, short=None):
        """Initialize the new Terminator(Argument)."""
        self.infomation = str(information)
        super(Terminator, self).__init__(description, False, short)
