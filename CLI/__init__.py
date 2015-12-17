# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/__init__.py

"""Command Line Interface (CLI)

A Python framework for managing command line argument parsing and
automatic usage documentation.
"""

from .Exceptions import Error
from .Argument   import Argument
from .Required   import Required
from .Default    import Default
from .Switch     import Switch
from .Flag       import Flag
from .Terminator import Terminator
from .List       import List

from .SingleMode import SingleMode
from .MultiMode import MultiMode


__all__ = [Error, Argument, Required, Default, Switch, Flag, Terminator, List,
        SingleMode, MultiMode]
