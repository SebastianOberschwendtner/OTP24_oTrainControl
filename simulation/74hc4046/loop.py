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
from scipy import signal, optimize
import matplotlib.pyplot as plt
from termcolor import cprint

# === Constants ===
# Matplotlib style
plt.style.use("fivethirtyeight")
# Valid execution modes
MODES = ["analyze", "design", "get_kvco", "step"]


# === Functions ===
def print_value(value: float, name: str, unit: str) -> None:
    """Prints a value with its name and unit.

    Args:
        value (float): The value to print.
        name (str): The name of the value.
        unit (str): The unit of the value.

    ---
    """
    print(f"{name + ':':20} {value:>14.2f} [{unit}]")


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


# === Classes ===
class HC4046:
    """Class for the 74HC4046 PLL loop.

    This class contains the parameters of the 74HC4046 PLL loop and provides
    functions to analyze and design the loop filter.

    Note:
        This class assumes that a passive RC lag-lead filter is used as the
        loop filter.

    ---
    """

    def __init__(self, *params) -> None:
        """Initializes the PLL loop.

        ---
        """
        self.k_vco = 1.0
        self.k_pd = 1.0
        self.k_n = 1.0
        self.r = [1.0, 1.0]
        self.c = [1.0]

        # Check if the parameters are given
        if len(params) == 1:
            # Set the parameters
            self.set_parameters(params[0])

    def set_parameters(self, parameters: dict) -> None:
        """Sets the parameters of the PLL loop.

        Args:
            parameters (dict): The parameters of the PLL loop.

        ---
        """
        # Set the parameters
        self.k_vco = parameters["S Parameters"]["k_vco"]

        # Switch for k_pd
        match parameters["Operating Conditions"]["Phase Detector"]:
            case "I":
                self.k_pd = parameters["Operating Conditions"]["Supply Voltage"] / np.pi
            case "II" | "III":
                self.k_pd = parameters["Operating Conditions"]["Supply Voltage"] / (2 * np.pi)

        # k_n
        self.k_n = (
            parameters["Operating Conditions"]["Input Frequency"]
            / parameters["Operating Conditions"]["Output Frequency"]
        )
        self.r = parameters["Loop Filter"]["R"]
        self.c = parameters["Loop Filter"]["C"]

    def get_transfer_function(self) -> signal.TransferFunction:
        """Calculates the transfer function of the PLL loop.

        Returns:
            signal.TransferFunction: The transfer function of the PLL loop.

        ---
        """
        # Create the transfer function
        num = [
            self.k_vco * self.k_pd * (self.tau[1] / (self.tau[0] + self.tau[1])),
            self.k_vco
            * self.k_pd
            * (self.tau[1] / (self.tau[0] + self.tau[1]))
            / self.tau[1],
        ]
        den = [
            1,
            (1 + self.k_n * self.k_pd * self.k_vco * self.tau[1])
            / (self.tau[0] + self.tau[1]),
            (self.k_n * self.k_pd * self.k_vco) / (self.tau[0] + self.tau[1]),
        ]
        return signal.TransferFunction(num, den)

    @property
    def tau(self) -> list[float]:
        """Calculates the time constants of the PLL loop.

        Returns:
            list[float]: [s] The time constants of the PLL loop.

        ---
        """
        # Calculate the time constants
        return [self.r[0] * self.c[0], self.r[1] * self.c[0]]

    @property
    def natural_frequency(self) -> float:
        """Calculates the natural frequency of the PLL loop in Hz.

        Returns:
            float: [Hz] The natural frequency of the PLL loop.

        ---
        """
        # Return the natural frequency
        return np.sqrt(
            (self.k_vco * self.k_pd * self.k_n) / (self.tau[0] + self.tau[1])
        )

    @property
    def damping_factor(self) -> float:
        """Calculates the damping factor of the PLL loop.

        Returns:
            float: [-] The damping factor of the PLL loop.

        ---
        """
        return (self.natural_frequency / 2) * (
            self.tau[1] + 1 / (self.k_vco * self.k_pd * self.k_n)
        )


# === Execution Modi ===
def design(parameters: dict) -> None:
    """Designs the PLL loop filter.

    Args:
        parameters (dict): The parameters from the json file.
    """
    # Inform the user
    cprint("Designing PLL Loop", "black", "on_green", attrs=["bold"])
    cprint("-> Fitting R1 and R2 values. C is taken from ", "yellow", end="")
    cprint("parameters.json.", "yellow", attrs=["bold"])
    pll = HC4046(parameters)

    # Define the residuals
    def residuals(x: list[float]) -> list[float]:
        # Update the pll parameters
        pll.r = x[:]

        # Convert the target frequency to rad/s
        target_frequency = parameters["Design"]["Natural Frequency"] * 2 * np.pi

        # Return the residuals
        return [
            pll.natural_frequency - target_frequency,
            pll.damping_factor - parameters["Design"]["Damping Factor"],
        ]

    # Optimize the loop filter resistance values
    result = optimize.least_squares(
        residuals,
        pll.r,
        bounds=(0, np.inf),
    )

    # Print the results
    if result.success:
        print_value(pll.r[0] * 1e-3, "R1", "kOhm")
        print_value(pll.r[1] * 1e-3, "R2", "kOhm")
        print_value(pll.c[0] * 1e12, "C", "pF")
    else:
        print("Optimization failed.")
        return

    # Analyze the loop filter
    print_value(1e-3 * pll.natural_frequency / (2 * np.pi), "Natural Frequency", "kHz")
    print_value(pll.damping_factor, "Damping Factor", "-")


def analyze(parameters: dict) -> None:
    """Analyzes the PLL loop filter.

    This function takes the parameters from the json file and analyzes the
    PLL loop filter. The natural frequency and damping factor are calculated
    and printed to the console.

    Args:
        pll (PLL): The pll loop to analyze.

    ---
    """
    # Inform the user
    cprint("PLL Loop", "black", "on_green", attrs=["bold"])

    # Print the PLL parameters
    pll = HC4046(parameters)
    print_value(1e-3 * pll.natural_frequency / (2 * np.pi), "Natural Frequency", "kHz")
    print_value(pll.damping_factor, "Damping Factor", "-")

    # Analyze the loop filter bandwidth
    cprint("Loop Filter", "black", "on_green", attrs=["bold"])
    w_3db = 1 / (pll.tau[0] + pll.tau[1])
    gain_pass = pll.tau[1] / (pll.tau[0] + pll.tau[1])
    print_value(1e-3 * w_3db / (2 * np.pi), "3 dB Bandwidth", "kHz")
    print_value(20* np.log(gain_pass), "Passband Gain", "dB")


def get_kvco(parameters: dict) -> None:
    """Extract the `k_vco` S parameter from the measured data.

    Args:
        parameters (dict): The parameters from the json file.

    ---
    """
    # Inform the user
    cprint("Extracting k_vco", "black", "on_green", attrs=["bold"])

    # Load the measured data
    vco_data = Path(__file__).parent / "vco.csv"
    print(f"Using data from: {vco_data}")
    data = np.loadtxt(vco_data, delimiter=",", skiprows=1)
    voltage = data[:, 0]
    frequency = data[:, 1] * 1e3  # Scale the frequency column from KHz to Hz

    # Get the index which is closed to the operating frequency
    index = np.argmax(frequency >= parameters["Operating Conditions"]["Output Frequency"])

    # Calculate the local slope in [Hz/V] using the three-point-midpoint formula
    grad = np.gradient(frequency, voltage)

    # Calculate the k_vco parameter
    k_vco = 2 * np.pi * grad[index]

    # Print the result
    print_value(k_vco * 1e-3, "k_vco", "kHz/V")


def step(parameters: dict) -> None:
    """Plots the step response of the PLL loop.

    Args:
        parameters (dict): The parameters from the json file.

    ---
    """
    # Inform the user
    cprint("Plotting Step Response", "black", "on_green", attrs=["bold"])

    # Create the PLL loop
    pll = HC4046(parameters)

    # Create the transfer function
    tf = pll.get_transfer_function()

    # Calculate the step response
    t, y = signal.step(tf)

    # Plot the step response
    _, ax = plt.subplots()
    ax.plot(t * 1e6, y)
    ax.set_xlabel("Time [us]")
    ax.set_ylabel("Amplitude [-]")
    ax.set_title("Step Response")
    ax.grid(True)
    plt.show()


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
