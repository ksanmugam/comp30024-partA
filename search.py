"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors:
"""

import sys
import json
import math
import operator
from queue import PriorityQueue

def main():

    with open(sys.argv[1]) as file:
        data = json.load(file)

    #Reads JSON data and stores coordinates of colour and "blocks"
    board = initial_board(data)

    print_board(board, message="", debug=True)


    a_star_search(board, (0,-1), data["colour"])





#Creates a board with initial json information
def initial_board(data):
    ran = range(-3, +3+1)
    board = {}
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        board[qr] = ""
    board.update({key: data.get("colour") for key in [tuple(l) for l in data["pieces"]]})
    board.update({key: "block" for key in [tuple(l) for l in data["blocks"]]})
    return board

#Heuristic to be ised in A*
def manhattan_distance(current_pos, colour):
    end_points = {  "red" : [(3,-3),(3,-2),(3,-1),(3,0)],
                    "green" : [(-3,3),(-2,3),(-1,3),(0,3)],
                    "blue" : [(-3,0),(-2,-1),(-1,-2),(0,-3)]
    }
    distances = []
    for i in end_points.get(colour):
        #euclidean = math.sqrt( (current_pos[0]-i[0])**2 + (current_pos[1]-i[1])**2 )
        manhattan = abs(current_pos[0]-i[0]) + abs(current_pos[1]-i[1])
        distances.append(manhattan)

    return min(distances)

#Calcualtes the possible moves excluding blocked tiles and including jumps
def possible_moves(current_pos, board, colour):
    #max range for coordinate values
    max_coord = range(-3,4)
    six_directions = [(0,-1),(1,-1),(1,0),(0,1),(-1,1),(-1,0)]
    #hard coded restricted coordinates in range but shouldn't be reachable
    restricted = [(-1,-3),(-2,-2),(-3,-1),(1,3),(2,2),(3,1)]
    next_pos = []

    for i in six_directions:
        temp_pos = tuple(map(operator.add, current_pos, i))
        look_ahead = tuple(map(operator.add, temp_pos, i))

        if(temp_pos[0] in max_coord) and (temp_pos[1] in max_coord):
            if(abs(temp_pos[0]) + abs(temp_pos[1]) <= 6):
                if(temp_pos not in restricted):
                    if(board[temp_pos] == "block"):
                        pass
                    elif((board[temp_pos] == colour) and (board[look_ahead] == colour)):
                        pass
                    elif((board[temp_pos] == colour) and (board[look_ahead] != colour)):
                        next_pos.append(look_ahead)
                    else:
                        next_pos.append(temp_pos)

        return next_pos


def a_star_search(board, start, colour):
    cost = 1
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from['start'] = None
    cost_so_far['start'] = 0

    end_points = {  "red" : [(3,-3),(3,-2),(3,-1),(3,0)],
                    "green" : [(-3,3),(-2,3),(-1,3),(0,3)],
                    "blue" : [(-3,0),(-2,-1),(-1,-2),(0,-3)]
                    }

    while not frontier.empty():
        current = frontier.get()

        if current in end_points[colour]:
            break

        for next in possible_moves(start, board, colour):
            new_cost = cost_so_far['start'] + cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + manhattan_distance(next, colour)
                frontier.put(next, priority)
                came_from[next] = current

    print ("This is the came_from:",came_from ,"\n")

    return came_from, cost_so_far




def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.

    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using
    the axial coordinate system outlined in the project specification) and the
    values are formatted as strings and placed in the drawing at the corres-
    ponding location (only the first 5 characters of each string are used, to
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}|
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}|
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}|
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}|
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}|
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}|
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} |
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-'
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
