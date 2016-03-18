# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/MultiMode.py

"""Implementation of the CLI MultiMode class."""

import os

from .Argument import Argument
from .Terminator import Terminator
from .Exceptions import Error, Usage

class MultiMode(object):
    """A MultiMode application has several subcommands, each of which is
    a SingleMode application in and of its self.
    """

    def __init__(self, argv):
        """Accepts the command line arguments *argv* (sys.argv)."""

        self.name = os.path.basename(argv[0])
        self.argv = argv[1:]
        self.info = None

        self.SubCommands = {}
        self.AllTerminators = []

        # default member, all MultiMode applications have this options
        self.help = Terminator("show this message", "", "h")


    def Exe(self, reassign=True, exceptions=False):
        """Parse the *argv* and run the called *subcommand*.

        reassign: bool
            After parsing the *argv*, *reassign* the member arguments
            to their *value*. (passed to the SingleMode *subcommand*s).

        exceptions: bool
            If true, re-raise the CLI.Error when caught.
        """

        try:

            self.rc()
            return self.SubCommands[self.argv[0]](self.argv).Exe(reassign=reassign,
                    exceptions=False)

        except Usage as usage:
            print(usage)
            return 0

        except Error as error:
            if exceptions:
                raise

            print(error)
            return 1

        except KeyError as error:
            print("`{}` is not an available subcommand!".format(self.argv[0]))
            return 2


    def rc(self):
        """Runtime configuration (parse *argv*)"""

        self.register()

        if not self.argv:
            raise Usage(self.usage_statement())

        if self.argv[0][0] == "-":
            self.interpret(self.argv[0])

        if self.help.given:
            raise Usage(self.help_statement())

        for name, arg in self.__dict__.items():
            if name in self.AllTerminators and arg.given:
                raise Usage(arg.information)


    def register(self):
        """Register all the member Arguments (strip self.__dict__ of non-Argument
        types). The only allowed member Arguments are Terminators.
        """

        self.Registry = {name: arg for name, arg in self.__dict__.items()
                if issubclass(type(arg), Argument)}

        for name, arg in self.Registry.items():

            if isinstance(arg, Terminator):
                self.AllTerminators.append(name)

            else:
                raise Error("Only Terminator(Argument) types are allowed as members of the "
                        "CLI.MultiMode. Anything else is ill-defined!")

        # attach a `name` to Argument if None
        for names in self.Registry:
            if not self.__dict__[names].name:
                self.__dict__[names].name = names

        # check for `name` clashes
        name_set = set([self.__dict__[arg].name for arg in self.Registry])
        if len(name_set) != len(self.Registry):
            raise Error("There is a *name* clash the Argument members of {}!".format(self.name))


    def interpret(self, flag):
        """Interpret a Terminator passed from rc()."""

        if len(flag) < 2:
            raise Error("'-' is not a valid flag!")

        if flag[1] == "-":

            if len(flag) < 3:
                raise Error("'--' is not a valid flag!")

            self.long_form(flag[2:])

        else:
            self.short_form(flag[1:])


    def long_form(self, flag):
        """Interpret a long form flag argument."""

        for arg in self.Registry:
            if self.__dict__[arg].name == flag:
                self.__dict__[arg].given = True
                return

        raise Error("--{} does not name a flag!".format(flag))


    def short_form(self, flag):
        """Interpret a short form flag argument."""

        for arg in self.Registry:
            if self.__dict__[arg].short and self.__dict__[arg].short == flag:
                self.__dict__[arg].given = True
                return

        raise Error("-{} does not name a flag!".format(flag))


    def usage_statement(self):
        """Generate the usage string for this application."""

        tab = " " * (7 + len(self.name))

        longest_subcommand = 0
        for command in self.SubCommands:
            if len(command) > longest_subcommand:
                longest_subcommand = len(command)

        message = "usage: {}".format(self.name)

        for command in self.SubCommands:
            message += " {}{} ...\n{}".format(command, " " * (longest_subcommand -
                len(command) + 2), tab)

        message += "\n{}".format(self.__doc__)
        return message


    def help_statement(self):
        """Generate the help string for this application."""

        message = self.usage_statement()

        spacing = 0
        for flag in self.AllTerminators:
            if len(self.__dict__[flag].name) > spacing:
                spacing = len(self.__dict__[flag].name)

        spacing += 10

        for flag in self.AllTerminators:
            message += self.__dict__[flag].help()

        if self.info:
            message += "\n{}".format(self.info)

        return message
