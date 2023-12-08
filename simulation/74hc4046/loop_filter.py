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
- *File:*     loop_filter.py
- *Details:*  Python 3.11
- *Date:*     2023-12-04
- *Version:*  v1.0.0

## Description
Simulation script for the 74HC4046 PLL loop filter.
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
import pathlib
import json
import argparse

# === Constants ===
# Valid execution modes
MODES = ["analyze", "design"]

# === Functions ===
def design():
    pass

def analyze():
    pass

# === Main ===
if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Design and simulation script for the 74HC4046 PLL loop filter."
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

    # Try calling the specified mode
    try:
        locals()[args.mode]()
    except NameError:
        # Invalid execution mode
        print(f"Invalid execution mode '{args.mode}'.")
