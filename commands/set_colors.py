#####################
# Dennis MUD        #
# set_colors.py   #
# Copyright 2020    #
# Michael D. Reiley #
#####################

# **********
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# **********

NAME = "set colors"
CATEGORIES = ["exploration", "settings"]
USAGE = "set colors [on|off]"
DESCRIPTION = """Check, enable, or disable colors.

If enabled, you will automatically get colors from the server.
Without an argument, just check the current setting.
Colors are currently not supported on browsers.

Ex. `set colors on` to enable ANSI colors."""


def COMMAND(console, args):
    # Perform initial checks.
    if not COMMON.check(NAME, console, args, argmin=0, argmax=1):
        return False

    # Just check our current colors setting.
    if len(args) == 0:
        if console.user["colors"]["enabled"]:
            console.msg("{0}: ANSI colors are currently enabled.".format(NAME))
        else:
            console.msg("{0}: ANSI colors are currently disabled.".format(NAME))
        return True

    # Make sure we chose an available option.
    if args[0].lower() in ["1", "enable", "enabled", "on", "true"]:
        console.user["colors"]["enabled"] = True
    elif args[0].lower() in ["0", "disable", "disabled", "off", "false"]:
        console.user["colors"]["enabled"] = False
    else:
        console.msg("{0}: Must choose one of: \"on\", \"off\".".format(NAME))
        return False
    console.database.upsert_user(console.user)

    # Finished.
    console.msg("{0}: Done.".format(NAME))
    return True
