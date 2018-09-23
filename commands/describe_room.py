from datatype import Room, User, Item

USAGE = "describe room <description>"
DESCRIPTION = "Set the description of the room you are in."


def COMMAND(console, database, args):
    if len(args) == 0:
        return False

    # Make sure we are logged in.
    if not console.user:
        return False

    roomid = console.user.room
    r = database.room_by_id(roomid)

    # Make sure we are the room's owner.
    if r.owner.lower() != console.user.name.lower():
        return False

    r.desc = ' '.join(args)
    database.update(r)
    return True
