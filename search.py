"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors:
Matthew Sy, 860032
Kirentheren Sanmugam, 823188

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


    #iterates through pieces and prints A* results
    for i in data["pieces"]:
        print_output(a_star_search(board, tuple(i), data["colour"]), board)


#Creates a board with initial json information
def initial_board(data):
    ran = range(-3, +3+1)
    board = {}
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        board[qr] = ""
    board.update({key: data.get("colour") for key in [tuple(l) for l in data["pieces"]]})
    board.update({key: "block" for key in [tuple(l) for l in data["blocks"]]})
    return board


#Heuristic that calculates number of steps to nearest exit
def hex_distance_end(current_pos, colour):
    end_points = {  "red" : [(3,-3),(3,-2),(3,-1),(3,0)],
                    "green" : [(-3,3),(-2,3),(-1,3),(0,3)],
                    "blue" : [(-3,0),(-2,-1),(-1,-2),(0,-3)]
                }
    distances = []
    for i in end_points.get(colour):
        #euclidean = math.sqrt( (current_pos[0]-i[0])**2 + (current_pos[1]-i[1])**2 )
        #manhattan = abs(current_pos[0]-i[0]) + abs(current_pos[1]-i[1])
        dx = current_pos[0] - i[0]
        dy = current_pos[1] - i[1]
        if sign(dx) == sign(dy):
            distances.append(abs(dx + dy))
        else:
            distances.append(max(abs(dx), abs(dy)))

    return min(distances)


#Heuristic which calculates distance between 2 positions
def hex_cost(current_pos, next):
    #return (math.sqrt( (current_pos[0]-next[0])**2 + (current_pos[1]-next[1])**2 ))
    dx = next[0] - current_pos[0]
    dy = next[1] - current_pos[1]

    if sign(dx) == sign(dy):
        return (abs(dx + dy))
    else:
        return (max(abs(dx), abs(dy)))


#Helper function used in hex distance calculations
def sign(num):
    if (num < 0):
        return -1
    elif (num > 0):
        return 1
    else:
        return 0


#Calculates the possible moves excluding blocked tiles and including jumps
def possible_moves(board, current_pos, colour):
    #max range for coordinate values
    max_coord = range(-3,4)
    six_directions = [(0,-1),(1,-1),(1,0),(0,1),(-1,1),(-1,0)]
    #Restricted coordinates in range but shouldn't be reachable
    restricted = [(-1,-3),(-2,-2),(-3,-1),(1,3),(2,2),(3,1)]
    next_pos = []

    for i in six_directions:
        #computes adjacent coordinate in the direction of i
        temp_pos = tuple(map(operator.add, current_pos, i))
        #computes the coordinate adjacent to the temp_pos in the i direction
        look_ahead = tuple(map(operator.add, temp_pos, i))

        #if next position available, add to next_pos list
        if(temp_pos[0] in max_coord) and (temp_pos[1] in max_coord):
            if(abs(temp_pos[0]) + abs(temp_pos[1]) <= 6):
                if(temp_pos not in restricted):
                    try:
                        if (board[temp_pos] == colour and board[look_ahead] == "block"):
                            pass
                        elif (board[temp_pos] == colour and board[look_ahead] == colour):
                            pass
                        elif (board[temp_pos] == "block" and board[look_ahead] == "block"):
                            pass
                        elif (board[temp_pos] == "block" and board[look_ahead] == ""):
                            next_pos.append(look_ahead)
                        elif (board[temp_pos] == colour and not board[look_ahead]):
                            next_pos.append(look_ahead)
                        elif (board[temp_pos] == "block" and board[look_ahead] == ""):
                            next_pos.append(look_ahead)
                        else:
                            next_pos.append(temp_pos)
                    except KeyError:
                        continue

    return next_pos


# A* adapted from https://www.redblobgames.com/pathfinding/a-star/implementation.html
def a_star_search(board, start, colour):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    priorities_done = []
    sequence = []

    end_points = {  "red" : [(3,-3),(3,-2),(3,-1),(3,0)],
                    "green" : [(-3,3),(-2,3),(-1,3),(0,3)],
                    "blue" : [(-3,0),(-2,-1),(-1,-2),(0,-3)]
                }
    #loop through unsearched paths with lowest cost so far
    while not frontier.empty():
        current = frontier.get()[1]
        sequence.append(current)
        board.update({current : colour})
        moves = possible_moves(board, current, colour)

        if current in end_points[colour]:
            break

        #Computes the new cost and priority for each position in moves
        for next in moves:
            new_cost = cost_so_far[current] + hex_cost(current, next)
            priority = new_cost + hex_distance_end(next, colour)

            #prevents equal priorities ie multiple same cost paths
            if priority in priorities_done:
                break
            #Updates the unexplored frontier with the new position and its current cost to goal as the priority
            elif next not in cost_so_far or new_cost < cost_so_far[next]:
                priorities_done.append(priority)
                cost_so_far[next] = new_cost
                frontier.put((priority, next))
                came_from[next] = current
                board.update({current : " "})

        priorities_done.clear()

    return sequence


#Prints output in required format
def print_output(list, board):
    ran = range(len(list))
    for i in ran:
        try:
            last = list[i+1]
        except IndexError:
            print("EXIT from {}.".format(list[i]))
            board.update({list[i] : " "})
            return
        if(hex_cost(list[i], list[i+1]) == 1):
            print("MOVE from {} to {}.".format(list[i], list[i+1]))
        elif(hex_cost(list[i], list[i+1]) == 2):
            print("JUMP from {} to {}.".format(list[i], list[i+1]))



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
