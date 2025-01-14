#######################
# Dennis MUD          #
# alter_item.py    #
# Copyright 2018-2020 #
# Michael D. Reiley   #
#######################

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

import random

NAME = "alter item"
CATEGORIES = ["items"]
USAGE = "alter item <item_id> <item_type>"
DESCRIPTION = """Set the type of the item with <item_id>.

Currently supported item types are:
- simple
- book
- container
- cursed
- radio

If the item type is not default then it's a special item like a book 
for learning languages. They don't necessarily need to look and used like a book.
Wizards can alter any item from anywhere. The item type simple basically resets the other types.

Ex. `alter item 4 book`
Ex2. `alter item 4 simple"""


def COMMAND(console, args):
    # Perform initial checks.
    if not COMMON.check(NAME, console, args, argmin=2):
        return False
    types=["simple", "book", "container", "cursed", "radio"]
    # Perform argument type checks and casts.
    itemid = COMMON.check_argtypes(NAME, console, args, checks=[[0, int]], retargs=0)
    if itemid is None:
        return False

    # Lookup the target item and perform item checks.
    thisitem = COMMON.check_item(NAME, console, itemid, owner=True, holding=True)
    if not thisitem:
        return False

    # alter the item.
    if args[1] not in types:
        console.msg("Not a valid item type. Currently items can be one of these: {0}".format(', '.join(types)))
        return False
    if args[1]=="simple":
        # Turning it into a simple item.
        # Turn off being a language book.
        thisitem["lang"] = None
        # Turn off curses.
        thisitem["cursed"]["enabled"] = False
        thisitem["cursed"]["cursetype"] = ""
        # Turn off radio vars.
        thisitem["radio"]["enabled"] = False
        thisitem["radio"]["frequency"] = 0
        # If its empty, turn off being a container.
        if(len(thisitem["container"]["inventory"]))>0:
            console.msg("Can't make it a non-container, please empty the item first.")
            return False
        else: thisitem["container"]["enabled"] = False

    elif args[1]=="radio":
        # Turn it into a radio or disable being one if it was already a radio.
        if thisitem["radio"]["enabled"]:
           thisitem["radio"]["enabled"] = False
           console.msg("{0} is not a radio from now.".format(thisitem["name"]))
        else:    
            thisitem["radio"]["enabled"] = True
            thisitem["radio"]["frequency"] = 0
            console.msg("{0} is now a radio".format(thisitem["name"]))

    elif args[1]=="book":
        thisitem["lang"] = console.user["lang"]
    elif args[1]=="cursed":
        if thisitem["cursed"]["enabled"]:
           thisitem["cursed"]["enabled"] = False
           console.msg("{0} is not cursed from now.".format(thisitem["name"]))
        else:    
            # Curses are random at the moment.
            # Spirit gain deny
            # Random direction when walking
            # Messing up inventory item names
            # Nightmare - spirit gain deny when asleep
            curses=["spirit","randomwalk","invmess","nightmare"]
            thisitem["cursed"]["enabled"] = True
            thisitem["cursed"]["cursetype"] = random.choice(curses)
            console.msg("{0} is now cursed with: {1}".format(thisitem["name"],thisitem["cursed"]["cursetype"]))

    elif args[1]=="container":
        if "into" in thisitem["name"] or "from" in thisitem["name"]:
            console.msg("Containers can't have the word INTO or FROM in their name. Please rename the item before making it a container.")
            return False
        if thisitem["container"]["enabled"]:
            if(len(thisitem["container"]["inventory"]))>0:
                console.msg("Can't make it a non-container, please empty the item first.")
                return False
            else:
                thisitem["container"]["enabled"] = False
                thisitem["container"]["inventory"] = []
        else:
            thisitem["container"]["enabled"] = True
            thisitem["container"]["inventory"] = []
    console.database.upsert_item(thisitem)

    # Finished.
    console.msg("{0}: Done.".format(NAME))
    return True
