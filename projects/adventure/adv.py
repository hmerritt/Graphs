from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
gr = {}


def dir_reverse(dir):
    reversed = {
        "n": "s",
        "s": "n",
        "e": "w",
        "w": "e"
    }
    return reversed[dir]

def arr_to_obj(arr, val = "?"):
    obj = {}
    for i in arr:
        obj[i] = val
    return obj

def gr_init_room():
    global player
    return arr_to_obj(player.current_room.get_exits())

def walk(dir):
    global player
    player.travel(dir)
    traversal_path.append(dir)
    return player.current_room.id

def has_traversed_room(room_id):
    global gr
    room = gr[room_id]
    for key, value in room.items():
        if value == "?":
            return False
    return True

def pick_room_to_enter():
    global player
    global gr
    for key, value in gr[player.current_room.id].items():
        if value == "?":
            return key
    return False


while True:
    room_id = player.current_room.id

    if len(gr) == 0:
        # add first room
        gr[room_id] = gr_init_room()
        gr[room_id]["bread_crum"] = []
    elif len(gr) >= 500 and room_id == 0:
        # complete traversal
        break

    # check if all rooms have been traversed
    if not has_traversed_room(room_id):
        # pick a room to enter
        traverse_dir = pick_room_to_enter()

        # travel to new room
        room_id_new = walk(traverse_dir)

        # init room
        if room_id_new not in gr:
            gr[room_id_new] = gr_init_room()

            # add 'bread_crum' of how to walk back faster
            bread_crum = dir_reverse(traverse_dir)
            gr[room_id_new]["bread_crum"] = [bread_crum]
        else:
            bread_crum = dir_reverse(traverse_dir)
            gr[room_id_new]["bread_crum"].append(bread_crum)

        # fill graph info
        gr[room_id][traverse_dir] = room_id_new
        gr[room_id_new][bread_crum] = room_id
    else:
        # use bread_crum to walk back
        if "bread_crum" in gr[room_id]:
            bread_crums = gr[room_id]["bread_crum"]
            room_id_new = walk(bread_crums[-1])
            if len(bread_crums) > 1:
                gr[room_id]["bread_crum"].pop()





################
# TRAVERSAL TEST
################
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
