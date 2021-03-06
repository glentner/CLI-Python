#!/usr/bin/env python3
# Copyright (c) Geoffrey Lentner 2015. All rights reserved.
# GNU General Public License v3.0, see LICENSE file.
# examples/hello.py

"""hello.py

Showcase the CLI.SingleMode API with a simple `hello, world!` example.
"""

import sys, CLI

class Hello(CLI.SingleMode):
    """A simple `hello, world!` style application to showcase the CLI.SingleMode API.
    Pass the -h | --help flag for more information.
    """

    # `self.__doc__` becomes the program description!

    def __init__(self, argv):
        """Pass the sys.argv parameter list to your __init__ method."""

        # you must first inherit the super class __init__ method.
        super(Hello, self).__init__(argv)

        # add your Arguments
        self.user      = CLI.List("user names")
        self.computer  = CLI.Switch("name of the computer", "Lisa", "c", name="computer-name")
        self.message   = CLI.Switch("the greeting", "how are you?", "m")
        self.verbose   = CLI.Flag("show output", False, "v")
        self.version   = CLI.Terminator("show version information", "hello.py (1.0.1)", "V")
        self.copyright = CLI.Terminator("show copyright information",
            "hello.py (1.0.1)\n"
            "Copyright (c) Geoffrey Lentner 2015. All rights reserved.\n"
            "GNU General Public License (v3.0).\n"
            "This is free software; see the source for copyright conditions. There is NO\n"
            "waranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.", "C")

        # if the `info` member is defined, it will be displayed at the end of a call to
        # -h | --help
        self.info = (""
                "Report bugs to: glentner@nd.edu\n"
                "home page: <http://github.com/glentner/CLI-Python>")


    def main(self):
        """The *main* function to be executed by the application."""

        if self.verbose:

            print("Incoming message from {}: 'Greetings:".format(self.computer), end="")

            if len(self.users) == 1:
                print(" {}".format(self.users[0]), end="")

            elif len(self.users) == 2:
                print(" {} and {}".format(*self.users), end="")

            else:
                print(" " + ", ".join(self.users[:-1]), end="")
                print(" and {}".format(self.users[-1]), end="")

            print("; {}'".format(self.message))

        return 0


if __name__ == "__main__":
    sys.exit( Hello(sys.argv).Exe() )
