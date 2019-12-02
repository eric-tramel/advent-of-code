import os
import sys

from collections import namedtuple
from pathlib import Path

INPUT_FILE = "../task-input.dat"

OP_END = 99
OP_ADD = 1
OP_MULT = 2

Operation =  namedtuple('Operation', 'opcode read_ptr_lhs read_ptr_rhs write_ptr')

def decode_op(program, program_pointer):
    """Decode a 4-value operation at the pointer.
    """
    if program[program_pointer] == OP_END:
        return Operation(OP_END, -1, -1, -1)
    else:
        return Operation(
            program[program_pointer],
            program[program_pointer+1],
            program[program_pointer+2],
            program[program_pointer+3]
        )

def run_generic_op(program, op, f):
    lhs = program[op.read_ptr_lhs]
    rhs = program[op.read_ptr_rhs]

    if op.write_ptr >= len(program):
        raise RuntimeError("Write location out-of-bounds")

    program[op.write_ptr] = f(lhs, rhs)


def run_add_op(program, op):
    run_generic_op(program, op, lambda x, y: x+y)

def run_mult_op(program, op):
    run_generic_op(program, op, lambda x, y: x*y)


def run_next_command(program, program_pointer):
    op = decode_op(program, program_pointer)
    if op.opcode == OP_ADD:
        print("ADD OP")
        run_add_op(program, op)
        program_pointer += 4
    elif op.opcode == OP_MULT:
        print("MULT OP")
        run_mult_op(program, op)
        program_pointer += 4
    elif op.opcode == OP_END:
        # End opeartion
        print("END PGRM")
        return -1
    else:
        raise ValueError(f"Invalid Operation {op}")
    return program_pointer

def run_program(program):
    program_pointer = 0

    while program_pointer >= 0:
        program_pointer = run_next_command(program, program_pointer)

    return program

def test_program_a():
    result = run_program([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    assert result == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]

def test_program_b():
    assert run_program([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
    assert run_program([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
    assert run_program([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
    assert run_program([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]

if __name__ == "__main__":
    # Run tests
    test_program_a()
    test_program_b()

    # Run the solution program
    input_file = Path(INPUT_FILE).resolve()

    # Get the program! 
    program = [int(m) for m in input_file.read_text().split(",")]


    # Make slight alteration...
    program[1] = 12
    program[2] = 2

    # Run program !
    run_program(program)

    # Program output?
    print(f"Final Output of 1202 Intcode Program: {program[0]}")







