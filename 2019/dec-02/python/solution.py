import os
import sys

from collections import namedtuple
from pathlib import Path
from itertools import product

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
    """Run a generic two-input operation defined by function f
    """
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
        run_add_op(program, op)
        program_pointer += 4
    elif op.opcode == OP_MULT:
        run_mult_op(program, op)
        program_pointer += 4
    elif op.opcode == OP_END:
        # End opeartion
        return -1
    else:
        raise ValueError(f"Invalid Operation {op}")
    return program_pointer

def run_program(program, in_a=None, in_b=None):
    """Run the specified program.

    The intcode program is given as a list, which can be thought 
    of as the program memory. For the structure of this program,
    memory locations 1 and 2 are the two inputs. After the 
    program halts, the final result is stored at the 0 index of
    the program.

    Parameters
    ----------

    program : list[int]
        A list of integers which represents the program memory.
    in_a : int 
        Optional input value (LHS)
    in_b : int
        Optional input value (RHS)

    Returns
    -------
    int :
        program output.
    """
    program_pointer = 0

    # Just a little bit of error catching to go with our tiny program
    # execution code :) 
    if in_a is not None:
        if in_a < 0 or in_a > 99:
            raise ValueError("LHS program input must be in range [0,99]")
        program[1] = in_a
    if in_b is not None:
        if in_b < 0 or in_b > 99:
            raise ValueError("LHS program input must be in range [0,99]")
        program[2] = in_b

    # Main program execution
    while program_pointer >= 0:
        program_pointer = run_next_command(program, program_pointer)

    # Final output always stored back at 0
    return program[0]

def verify_program(prog_mem_in, target_prog_mem_out):
    """Give a program and what it should be. If it doesn't match,
    throw an error.
    """
    prog_mem_out = prog_mem_in.copy()
    run_program(prog_mem_out)
    assert prog_mem_out == target_prog_mem_out

def test_program_a():
    verify_program(
        [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
        [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    )

def test_program_b():
    verify_program(
        [1, 0, 0, 0, 99],
        [2, 0, 0, 0, 99]
    )
    verify_program(
        [2, 3, 0, 3, 99],
        [2, 3, 0, 6, 99]
    )
    verify_program(
        [2, 4, 4, 5, 99, 0],
        [2, 4, 4, 5, 99, 9801]
    )
    verify_program(
        [1, 1, 1, 4, 99, 5, 6, 0, 99],
        [30, 1, 1, 4, 2, 5, 6, 0, 99]
    )

if __name__ == "__main__":
    # Run tests
    test_program_a()
    test_program_b()

    # Run the solution program
    input_file = Path(INPUT_FILE).resolve()

    # Get the program! 
    program = [int(m) for m in input_file.read_text().split(",")]


    # Run program !
    program_return = run_program(program.copy(), in_a=12, in_b=2)

    # Program output?
    print(f"Final Output of 1202 Intcode Program: {program_return}")


    # Now, we need to find a combination of inputs to give us 
    # the value 19690720. Let's just do this the brute force way
    # without being smart.
    target_output = 19690720
    for a, b in product(range(100), range(100)):
        program_return = run_program(program.copy(), in_a=a, in_b=b)
        if program_return == target_output:
            break

    print(f"Inputs ({a}, {b}) produce output {target_output}")
    print(f"Solution = 100*{a} + {b} = {100*a+b}")
