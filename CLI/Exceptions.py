# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/Exceptions.py

"""
Exceptions for the CLI framework.
"""

class Error(Exception):
    """Generic Error object for CLI."""
    pass

class Usage(Exception):
    """Call to halt execution."""
    pass
