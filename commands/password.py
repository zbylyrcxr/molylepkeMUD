######################
# Dennis MUD         #
# password.py        #
# Copyright 2020     #
# Michael D. Reiley  #
######################

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

import hashlib

NAME = "password"
CATEGORIES = ["users"]
USAGE = "password [username] <password>"
DESCRIPTION = """Change your password.

You must be logged in. The username argument is optional.
Only wizards can change the passwords of other users.

Ex. `password n3wp4ss`
Ex2. `password seisatsu n3wp4ss`"""


def COMMAND(console, args):
    # Perform initial checks.
    if not COMMON.check(NAME, console, args, argmin=1, argmax=2):
        return False

    # Change our own password.
    if len(args) == 1 or (len(args) == 2 and args[0].lower() == console.user["name"]):
        console.user["passhash"] = hashlib.sha256(args[len(args)-1].encode()).hexdigest()
        console.database.upsert_user(console.user)

    # Trying to change someone else's password.
    elif not console.user["wizard"]:
        console.msg(NAME + ": only a wizard can change another user's password")
        return False

    # We have permission, so change another user's password.
    else:
        u = console.shell.user_by_name(args[0].lower())
        if not u:
            console.msg(NAME + ": no such user")
            return False
        u["passhash"] = hashlib.sha256(args[1].encode()).hexdigest()
        console.database.upsert_user(u)

    # Finished.
    console.msg(NAME + ": done")
    return True