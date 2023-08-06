"""
This module handles loading of lookup tables (LUT).

Every LUT is stored inside the LUTS dictionary object with its name as the
key. The value inside the dictionary is equal to an array, which specifies how
should pixel values be translated.

The .lut file specifying the transformations looks like:
0;0;0;0         # 0 ~> RGB(0, 0, 0)
1;43;28;4       # 1 ~> RGB(43, 28, 4)
2;57;35;5       # 2 ~> RGB(57, 35, 5)
...

"""
import sys
from importlib.resources import files
from os import listdir
from os.path import isdir
from pathlib import Path
from typing import TextIO

import numpy as np
from numpy.typing import ArrayLike, NDArray

LUT = ArrayLike
LUTS = dict()


def add_file(file_descriptor: TextIO, name: str) -> None:
    """
    Takes a text stream containing a LUT definition and adds to the global
    LUT repository.

    Parameters
    ----------
    file_descriptor: TextIO
        Text stream from which the data is loaded.
    name: str
        Name of the LUT table.

    """
    # Load the LUT
    file_lut = [0 for _ in range(256)]
    for line in file_descriptor:
        parts = [int(x) for x in line.rstrip().split(";")]
        val, map_val = parts[0], parts[1:]
        file_lut[val] = map_val
    file_lut = np.array(file_lut)
    LUTS[name] = file_lut


def add_luts_at_path(path_to_luts: str) -> None:
    """
    Loads all .lut files at the given directory.

    Parameters
    ----------
    path_to_luts: str
        Path to the directory containing the .lut files.

    """
    if not isdir(path_to_luts):
        raise RuntimeWarning(f"{path_to_luts} is not a directory!")

    for file in listdir(path_to_luts):
        if path_to_luts is None:
            file = str(file)

        if not file.endswith(".lut"):
            print(
                f"Warning: Skipped f{file} as it does not end with \'.lut\'.",
                file=sys.stderr)
            continue

        # Create name
        name = Path(file).stem.capitalize()
        try:
            with open(path_to_luts + file) as file_input:
                add_file(file_input, name)
        except OSError:
            print(f"Warning: Failed to load {name}! Skipping...")


def fill_luts() -> None:
    """
    Loads all LUTs included in the package.
    """
    resource = files("primawera.luts")
    if not resource.is_dir():
        raise RuntimeWarning("Cannot find LUTs resource inside the package!")

    for resource_file in resource.iterdir():
        if not resource_file.name.endswith(".lut"):
            print(
                f"Warning: Skipped f{resource_file} as it does not end with \'"
                f".lut\'.",
                file=sys.stderr)
            continue

        # Create name
        name = resource_file.name.capitalize()

        try:
            with open(resource_file) as file_input:
                add_file(file_input, name)
        except OSError:
            print(f"Warning: Failed to load LUT with {name}. Skipping...")


def get_lut(name: str) -> LUT:
    """
    Get LUT with the given name.

    Parameters
    ----------
    name: str
        Name of the LUT.

    Returns
    -------
    lut: LUT
        LUT with the given name if one exists otherwise returns an empty array.

    """
    return LUTS.get(name, [])


def apply_lut(data: NDArray[np.uint8], lut: LUT) -> ArrayLike:
    """
    Apply LUT to grayscale data.

    Parameters
    ----------
    data: uint8 2D ndarray.
        Data to apply LUT onto.
    lut: LUT
        LUT to apply.

    Returns
    -------
    out: uint8 2D ndarray
        New array with changed values.

    """
    result = lut[data]
    return result.astype(np.uint8)


if __name__ == "__main__":
    add_luts_at_path("luts/")
    lut = get_lut("Sepia")
    print(lut)
    a = (np.random.rand(10, 10) * 255).astype(np.uint8)
    print(a)
    print(apply_lut(np.array([a]), lut))
