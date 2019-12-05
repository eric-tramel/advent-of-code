import os
import sys
import itertools

from pathlib import Path
from functools import reduce

# Some Globals
DIR_UP = "U"
DIR_DN = "D"
DIR_L = "L"
DIR_R = "R"
DIR_SIGN = {
    DIR_UP: 1,
    DIR_DN: -1,
    DIR_L: -1,
    DIR_R: 1
}
DIR_DIM = {
    DIR_UP: 1,
    DIR_DN: 1,
    DIR_L: 0,
    DIR_R: 0
}
INPUT_FILE = "../task-input.dat"

def distance(point_a, point_b):
    """Calculate the Manhattan Distance between points.
    """
    dims = len(point_a)
    if len(point_b) != dims:
        raise ValueError("Points are of two different dimensions.")

    diffs = [abs(a - b) for a, b in zip(point_a, point_b)]
    return reduce(lambda x, y: x+y, diffs)

def decode_wire_str(wire_str):
    """Decode a wire string token.
    """
    direction = wire_str[:1]
    distance = int(wire_str[1:])
    return (direction, distance)

def line_from_token(start_point, token):
    """Get a line from a start point and a direction.
    """
    d = token[0]
    l = token[1]
    end_point = list(start_point)
    end_point[DIR_DIM[d]] += DIR_SIGN[d]*l
    
    return (tuple(start_point), tuple(end_point))

def tokens_to_lines(token_list):
    """Convert list of tokens into a list of lines.
    """
    cur_point = (0, 0)
    lines = []
    for token in token_list:
        line = line_from_token(cur_point, token)
        lines.append(line) 
        cur_point = line[1]
    return lines

def is_horz(line):
    """ Is a line horizontal? (equal y axis)
    """
    return line[0][1] == line[1][1]

def inrange(x, lo, hi):
    return x >= lo and x <= hi

def get_intersection(line_a, line_b):
    """We need to determine if there is an intersection. 
    And if so, we need to report where that intersection is.
    Otherwise, lets return None or something.

    On this grid, how many kinds of intersection can we have?
    1. Only (H,L), (L,H) pairs can intersect (assuming no direct
    overlap of the wires.)
    """
    intersect_point = None
    # Have to have different directions
    if is_horz(line_a) != is_horz(line_b):
        # Now we need to see if they extend long enough to overlap
        if is_horz(line_a):
            H = line_a
            V = line_b
        else:
            H = line_b
            V = line_a

        # The x of vert needs to be in the x range of horz
        # The y of horz needs to be in the y range of vert
        # And if this is the case, the intersection is the 
        # x of the vert and the y of the horz
        if inrange(V[0][0], H[0][0], H[1][0]) and inrange(H[0][1], V[0][1], V[1][0]):
            intersect_point = (V[0][0], H[0][1])
   
    return intersect_point


if __name__ == "__main__":
   
    # Get inputs
    input_file = Path(INPUT_FILE).resolve()
    wire_descriptions = [wire for wire in input_file.read_text().split("\n")][:-1]
    num_wires = len(wire_descriptions)
    print(f"Found {num_wires} in wiring chart.")
    
    # Now tokenize the wire descriptions.
    for i in range(num_wires):
        wire_descriptions[i] = [decode_wire_str(t) for t in wire_descriptions[i].split(",")]
        wire_descriptions[i] = tokens_to_lines(wire_descriptions[i])

    # Can we now get the list of intersections in a crazy fashion?
    # We need to loop over wires, check them against each other wire.
    # So we need to,really, make a big list of the line segments for the 
    # entire problem (we now have a big stack of line segments) and 
    # check the product of all of these with eachother, but not checking
    # one against itself again.
    intersections = []
    all_line_segments = list(itertools.chain.from_iterable(wire_descriptions))
    n_lines = len(all_line_segments)

    for i in range(n_lines):
        for j in range(n_lines):
            if i != j:
                x = get_intersection(all_line_segments[i], all_line_segments[j])
                if x is not None:
                    intersections.append(x)

    dist_from_zero = [abs(point[0]) + abs(point[1]) for point in intersections]
    dist_from_zero.sort()

    # Get the minimum value
    print(f"The minimum Manhattan distance to an intersection from (0,0) is {dist_from_zero[0]}")

    # Got 36 but it isn't right, so need to go back to the start




