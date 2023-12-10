#!python
# oTrainControl - Open Train Controller and Decoder
# Copyright (c) 2023 Sebastian Oberschwendtner, sebastian.oberschwendtner@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
### Details
- *File:*     loop.py
- *Details:*  Python 3.11
- *Date:*     2023-12-04
- *Version:*  v1.0.0

## Description
Simulation and design script for the 74HC4046 PLL loop.
The script can be used to:
- Generate a plot of the loop filter step response.
- Analyze the natural frequency and damping factor of the PLL loop.
- Design the loop filter for a given natural frequency and damping factor.

### Author
Sebastian Oberschwendtner, :email: sebastian.oberschwendtner@gmail.com

---
## Code

---
"""
# === Imports ===
from pathlib import Path
import json
import argparse
import numpy as np
from scipy import signal
from termcolor import cprint

# === Constants ===
# Valid execution modes
MODES = ["analyze", "design"]


# === Functions ===
def pll_transfer_function(parameters: dict) -> signal.TransferFunction:
    """Creates the transfer function of the PLL loop.

    Args:
        parameters (dict): The parameters from the json file.

    Returns:
        signal.TransferFunction: The transfer function of the PLL loop.
    """
    # Save the parameters
    k_vco: float = parameters["S Parameters"]["k_vco"]
    k_pd: float = parameters["S Parameters"]["k_pd"]
    k_n: float = parameters["S Parameters"]["k_n"]
    filter_type: str = parameters["Loop Filter"]["Type"]
    r_filter: list[float] = parameters["Loop Filter"]["R"]
    c_filter: list[float] = parameters["Loop Filter"]["C"]

    # Check the filter type
    if filter_type.lower() != "passive":
        raise NotImplementedError(
            f"Filter type '{filter_type}' is not implemented."
        )

    # Create the transfer function
    tau = r_filter[0] * c_filter[0]
    num = [k_vco * k_pd, k_vco * k_pd]
    den = [tau**2, 2 * tau, 1 + k_vco * k_pd * tau, k_vco * k_pd]
    return signal.TransferFunction(num, den)


def get_natural_frequency(pole: complex | list) -> float | list:
    """Calculates the natural frequency of the given pole in Hz.

    Args:
        pole (complex | list): The pole(s) to calculate the natural frequency for.

    Returns:
        float | list: [Hz] The natural frequency of the given pole(s).

    ---
    """
    return np.abs(pole) / (2 * np.pi)


def get_damping_factor(pole: complex | list) -> float | list:
    """Calculates the damping factor of the given pole.

    Args:
        pole (complex | list): The pole(s) to calculate the damping factor for.

    Returns:
        float | list: [-] The damping factor of the given pole(s).

    ---
    """
    return np.arctan2(pole.imag, pole.real) / np.pi


# === Execution Modi ===
def design(parameters: dict) -> None:
    pass


def analyze(parameters: dict) -> None:
    """Analyzes the PLL loop filter.

    This function takes the parameters from the json file and analyzes the
    PLL loop filter. The natural frequency and damping factor are calculated
    and printed to the console.

    Args:
        parameters (dict): The parameters from the json file.

    ---
    """
    # Inform the user
    cprint("Analyzing PLL Loop", "black", "on_green", attrs=["bold"])

    # Print the results
    for i, pole in enumerate(pll_transfer_function(parameters).poles):
        cprint(f"Pole: {i}", "white", "on_blue", attrs=["bold"])
        print(f"{'Natural frequency:':20} {get_natural_frequency(pole):>14.2f} [Hz]")
        print(f"{'Damping factor:':20} {get_damping_factor(pole):>14.2f} [-]")


# === Main ===
if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Design and simulation script for the 74HC4046 PLL loop."
    )

    # Add the arguments for the mode
    parser.add_argument(
        "mode",
        metavar="mode",
        type=str,
        choices=MODES,
        help="The execution mode of the script.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Read the parameters from the json file
    with open(Path(__file__).parent / "parameters.json", "r", encoding="utf-8") as file:
        json_parameters = json.load(file)

    # Try calling the specified mode
    try:
        locals()[args.mode](json_parameters)
    except NameError:
        # Invalid execution mode
        print(f"Invalid execution mode '{args.mode}'.")
