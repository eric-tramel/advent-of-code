import os
import sys 

from pathlib import Path
from functools import reduce

INPUT_FILE = "../task-input.dat"

def required_fuel_for_mass(mass):
    """Calculate fuel requirements for a given mass.

    If the estimate would be negative, according to the 
    original fuel mass calculation, report a cost of 0.

    Parameters
    ----------

    mass : int
        Mass for which to calculate the fuel requirement

    Returns
    -------

    int
        Fuel requirements (represnted as mass)
    """
    fuel_mass = mass // 3 - 2

    return fuel_mass if fuel_mass > 0 else 0

def required_fuel_for_module(module_mass):
    """Calculate total fuel required for a mass, thanks to the
    rocket equation...fuel begets more mass begets more fuel.

    Parameters
    ----------
    
    module_mass : int
        The mass of the module

    Returns
    -------

    int: 
        Total fuel mass, taking into account the mass of the fuel itsself.
    """
    fuel_mass = required_fuel_for_mass(module_mass)
    total_fuel_mass = fuel_mass
    while required_fuel_for_mass(fuel_mass) > 0:
        fuel_mass = required_fuel_for_mass(fuel_mass) 
        total_fuel_mass += fuel_mass
    
    return total_fuel_mass
    

def fuel_tally(fuels):
    return reduce(lambda a,b: a+b, fuels)

def test_required_fuel_for_mass():
    assert required_fuel_for_mass(12) == 2
    assert required_fuel_for_mass(14) ==  2
    assert required_fuel_for_mass(1969) == 654
    assert required_fuel_for_mass(100756) == 33583

def test_required_fuel_for_module():
    assert required_fuel_for_module(14) == 2
    assert required_fuel_for_module(1969) == 966
    assert required_fuel_for_module(100756) == 50346

if __name__ == "__main__": 
    # Run tests first
    print("Running tests...")
    test_required_fuel_for_mass()
    test_required_fuel_for_module()

    # Run the solution program
    input_file = Path(INPUT_FILE).resolve()

    # Let's just do things with numpy and try to be idiomatic 
    masses = [int(m) for m in input_file.read_text().split()]
    fuels_a = [required_fuel_for_mass(m) for m in masses]

    # Lets have fun with reduce!
    total_fuel_cost_a = fuel_tally(fuels_a)

    # Solution Reporting: Part A
    print(f"Total Fuel Estimate (Part A): {total_fuel_cost_a}")

    # Now lets do a bit better
    fuels_b = [required_fuel_for_module(m) for m in masses]
    total_fuel_cost_b = fuel_tally(fuels_b)

    # Solution Reporting: Part B
    print(f"Total Fuel Estimate (Part B): {total_fuel_cost_b}")