#####################
# Dennis MUD        #
# teleport.py       #
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

NAME = "teleport"
CATEGORIES = ["exploration"]
ALIASES = ["tp"]
USAGE = "teleport <room>"
DESCRIPTION = """Teleport to the room with ID <room>.

Anyone can teleport to room 0, but otherwise you can only teleport to a room that you own.

Ex. `teleport 0` to go to the first room.
Ex2. `teleport 17` to go to room 17."""


def COMMAND(console, database, args):
    if len(args) == 0:
        console.msg("Usage: " + USAGE)
        return False

    # Make sure we are logged in.
    if not console.user:
        console.msg(NAME + ": must be logged in first")
        return False

    try:
        dest = int(args[0])
    except ValueError:
        console.msg("Usage: " + USAGE)
        return False

    roomid = console.user["room"]
    thisroom = database.room_by_id(roomid)
    destroom = database.room_by_id(dest)

    if not destroom:
        console.msg(NAME + ": destination room does not exist")
        return False  # The destination room does not exist.
    if not console.user["name"] in destroom["owners"] and not console.user["wizard"] and not destroom["id"] == 0:
        console.msg(NAME + ": you do not have permission to teleport to that room")
        return False
    # Move us to the new room.
    if thisroom and console.user["name"] in thisroom["users"]:
        thisroom["users"].remove(console.user["name"])
    if console.user["name"] not in destroom["users"]:
        destroom["users"].append(console.user["name"])
    if thisroom:
        console.broadcast_room(console.user["nick"] + " vanished from the room")
    console.user["room"] = destroom["id"]
    console.broadcast_room(console.user["nick"] + " entered the room")
    if thisroom:
        database.upsert_room(thisroom)
    database.upsert_room(destroom)
    database.upsert_user(console.user)
    console.command("look", False)
    return True
