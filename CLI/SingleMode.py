# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# CLI/SingleMode.py

"""Implementation of the SingleMode class."""

import os

from .Argument   import Argument
from .Required   import Required
from .Default    import Default
from .Switch     import Switch
from .Flag       import Flag
from .Terminator import Terminator
from .List       import List
from .Exceptions import Error, Usage

class SingleMode(object):
    """A SingleMode application is one for which there is a single,
    primary execution mode. The SingleMode object is intended to be
    a parent class.
    """

    def __init__(self, argv):
        """Accepts the command line arguments *argv* passed to *main*."""

        self.name = os.path.basename(argv[0])
        self.argv = list(argv[1:])
        self.info = None

        self.Remainder      = {}
        self.GivenSwitches  = {}

        self.AllRequired    = []
        self.AllDefaults    = []
        self.AllSwitches    = []
        self.AllFlags       = []
        self.AllTerminators = []
        self.AllLists       = []

        # default member, all SingleMode applications have this option
        self.help = Flag("show this message", False, "h")


    def register(self):
        """Register all the member Arguments. Strip self.__dict__ of non-Argument
        types.
        """

        self.Registry = {name: arg for name, arg in self.__dict__.items()
                if issubclass(type(arg), Argument)}

        for name, arg in self.Registry.items():

            if isinstance(arg, Required):
                self.AllRequired.append(name)

            elif isinstance(arg, Default):
                self.AllDefaults.append(name)

            elif isinstance(arg, Switch):
                self.AllSwitches.append(name)

            elif isinstance(arg, Flag):
                self.AllFlags.append(name)

            elif isinstance(arg, Terminator):
                self.AllFlags.append(name)
                self.AllTerminators.append(name)

            elif isinstance(arg, List):
                self.AllLists.append(name)

            else:
                raise Error("Untracked Argument type for SingleMode."
                        "{} is not implementented.".format(type(arg)))

            if len(self.Registry) < 1:
                raise Error("There were no member Arguments defined for this "
                        "application! This program can never run!")

            if len(self.AllLists) > 1:
                raise Error("There can only be one List argument! Having more "
                        "than one List is an ill-defined application.")

            # attach a `name` member to all Argument members
            for names in self.Registry:
                if not self.__dict__[names].name:
                    self.__dict__[names].name = names

            # check the *default* value types for boolean Flags
            for names in self.AllFlags:
                if type(self.__dict__[names].default) is not bool:
                    raise Error("For Flag(Argument) `{}`: the *default* value must "
                            "be of {}".format(names, bool))

            # Flags must have a single character `short` for the flag stacking to work
            for arg in self.Registry:
                if self.__dict__[arg].short and len(self.__dict__[arg].short) != 1:
                    raise Error("For `{}`: the *short* form name should be a single "
                         "character in length!".format(arg))

            # no Arguments can share a `name`
            name_set = set([self.__dict__[arg].name for arg in self.Registry])
            if len(name_set) != len(self.Registry):
                raise Error("There was an Argument *name* clash in {}".format(self.name))


    def rc(self):
        """Runtime configuration (parse *argv*)"""

        self.register()

        if not self.argv:
            raise Usage(self.usage_statement())

        # identify the switches and flags
        for i, arg in enumerate(self.argv):
            if arg[0] == "-":
                if len(arg) < 2:
                    raise Error("'-' is not a recognized flag or switch!")

                self.interpret(i, arg[1:])
            else:
                self.Remainder[i] = arg

        if self.help.given:
            raise Usage(self.help_statement())

        for flag in self.AllTerminators:
            if self.__dict__[flag].given:
                raise Usage(self.__dict__[flag].information)

        # walk the switches and assign values
        for i, switch in self.GivenSwitches.items():

            if i + 1 not in self.Remainder:
                if len(self.argv) <= i + 1:
                    raise Error("--{} expected a free argument to follow but there were "
                            "none left!".format(switch))
                else:
                    raise Error("--{} expected a free argument to follow but found "
                            "`{}` instead!".format(switch, self.argv[i+1]))

            self.__dict__[switch].set(self.Remainder[i+1])
            del(self.Remainder[i+1])

        if len(self.Remainder) < len(self.AllRequired):
            raise Error("Insufficient arguments given: {} have not been provided."
                .format(", ".join(['`{}`'.format(arg) for arg in
                self.AllRequired[len(self.AllRequired) - len(self.Remainder):]])))

        self.Remainder = list(self.Remainder.values())

        # assign the Required arguments and pop them off the list
        for arg in self.AllRequired:
            self.__dict__[arg].set(self.Remainder[0])
            del(self.Remainder[0])

        if len(self.Remainder) > len(self.AllDefaults) and len(self.AllLists) == 0:
            raise Error("Too many arguments given! Only {} default arguments available "
                    "but {} given.".format(len(self.AllDefaults), len(self.Remainder)))

        # assign the Default arguments and pop them off the list
        for arg in self.AllDefaults:
            if len(self.Remainder) > 0:
                self.__dict__[arg].set(self.Remainder[0])
                del(self.Remainder[0])

        if len(self.Remainder) == 0 and len(self.AllLists) == 0:
            return

        if len(self.Remainder) > 0 and len(self.AllLists) == 0:
            raise Error("There were {} too many arguments!".format(len(self.Remainder)))

        if len(self.Remainder) == 0 and len(self.AllLists) > 0:
            raise Error("Expected at least one argument for `{}`!".format(self.AllLists[0]))

        # pass the remaining argument to the list
        self.__dict__[self.AllLists[0]].set(self.Remainder)


    def interpret(self, index, option):
        """Interpret Flags, Switches passed from *argv*."""

        if (option[0] == '-'):

            if len(option) < 2:
                raise Error("'--' is not a recognized flag or switch!")

            self.long_form(index, option[1:])

        else:
            self.short_form(index, option)



    def short_form(self, index, option):
        """Interpret a short form flag argument."""

        if len(option) > 1:
            # allow for stacked flags
            for flag in option[1:]:
                if not self.set_flag(flag):
                    raise Error("`{}` does not name a flag!".format(flag))

        elif not self.set_flag(option):
            if not self.set_switch(index, option):
                raise Error("`{}` does not name a flag or switch!".format(option))



    def set_flag(self, option):
        """Attempt to set a flag, return False on failure."""

        found = False
        for flag in self.AllFlags:
            if self.__dict__[flag].short and self.__dict__[flag].short == option:

                if self.__dict__[flag].given:
                    raise Error("The `{}` flag was already given!".format(flag))

                self.__dict__[flag].value = True
                self.__dict__[flag].given = True
                found = True
                break

        return found



    def set_switch(self, index, option):
        """Attempt to set a switch, return False on failure."""

        found = False
        for switch in self.AllSwitches:
            if self.__dict__[switch].short and self.__dict__[switch].short == option:

                if self.dict__[switch].given:
                    raise Error("The `{}` switch was already given!".format(switch))

                self.GivenSwitches[index] = switch
                self.__dict__[switch].given = True
                found = True
                break

        return found



    def long_form(self, index, option):
        """Set an argument given it's long form name."""

        # attempt to assign a flag first
        for arg in self.__dict__:
            if (issubclass(type(self.__dict__[arg]), Argument) and
                    self.__dict__[arg].name == option):

                if isinstance(self.__dict__[arg], Flag):

                    if self.__dict__[arg].given:
                        raise Error("The `{}` flag was already given!".format(option))

                    self.__dict__[arg].set(True)
                    self.__dict__[arg].given = True
                    return

                elif isinstance(self.__dict__[arg], Switch):

                    if self.__dict__[arg].given:
                        raise Error("The `{}` switch was already given!".format(arg))

                    self.GivenSwitches[index] = arg
                    self.__dict__[arg].given = True
                    return

        raise Error("--{} does not name a flag or switch!".format(option))



    def usage_statement(self):
        """Display a usage statement for the application."""

        message = "usage: {}".format(self.name)

        for arg in self.AllRequired:
            message += " {}".format(arg)

        for arg in self.AllDefaults:
            message += " [{} {}]".format(arg, self.__dict__[arg].default)

        for arg in self.AllLists:
            message += " {0}1 [{0}2 ...]".format(arg)

        for arg in self.AllSwitches + self.AllFlags:
            if self.__dict__[arg].short:
                message += " [-{} | --{} {}]".format(self.__dict__[arg].short, arg,
                        self.__dict__[arg].default)
            else:
                message += " [--{} {}]".format(arg, self.__dict__[arg].default)

        doc_lines = [line.strip() for line in self.__doc__.split("\n")]
        if not doc_lines[-1]:
            # on multiline docstrings the last line is empty
            del(doc_lines[-1])

        return "{}\n\n{}".format(message, "\n".join(doc_lines))


    def help_statement(self):
        """Show help information for this application (called with -h | --help)."""

        spacing = 0
        for names in self.Registry:
            if len(names) > spacing:
                spacing = len(names)

        spacing += 10
        message  = self.usage_statement()

        for arg in self.AllRequired:
            message += self.__dict__[arg].help(spacing)

        for arg in self.AllDefaults:
            message += self.__dict__[arg].help(spacing)

        for arg in self.AllLists:
            message += self.__dict__[arg].help(spacing)

        # additional spacing seperates nameless arguments from switches/flags
        message += "\n"

        for arg in self.AllSwitches:
            message += self.__dict__[arg].help(spacing)

        for arg in self.AllFlags:
            message += self.__dict__[arg].help(spacing)

        if self.info:
            message += "\n{}".format(self.info)

        return message


    def main(self):
        """*main* must be redefined for a SingleMode application!"""
        raise Error("*main* must be redefined for a SingleMode application!")


    def Exe(self, reassign=True, exceptions=False):
        """Parse the *argv* and run *main*.

        reassign: bool
            After parsing the *argv*, *reassign* the member arguments
            to their *value*.

        exceptions: bool
            If True, re-raise the CLI.Error when caught.
        """

        try:
            self.rc()

            if reassign:
                for name, arg in self.__dict__.items():
                    if issubclass(type(arg), Argument):
                        self.__dict__[name] = arg.value

            return self.main()

        except Usage as usage:
            print(usage)
            return 0

        except Error as err:

            if exceptions:
                raise

            print(err)
            return 1
