from typing import Tuple

import numpy as np # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb
graphic_dt = np.dtype( # dtype creates a data type that numpy can use
    [
        ("ch", np.int32), # Unicode codepoint; translates value from int to unicode
        ("fg", "3B"), # 3 unsigned bytes, for RGB colors
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data
tile_dt = np.dtype(
    [
        ("walkable", np.bool), # True if this tile can be walked over
        ("transparent", np.bool), # True if this tile doesn't block FOV
        ("dark", graphic_dt), # Graphics for when this tile isn't in FOV
        ("light", graphic_dt), # Graphics for when the file is in FOV
    ]
)

def new_tile(
        *, # Enforce the use of keywords so that parameter order doesn't matter
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types; creates a numpy array of one tile_dt element and returns it """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True, 
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (0, 0, 100), (50, 50, 150)),
    light=(ord(">"), (255, 255, 255), (200, 180, 50)),
)