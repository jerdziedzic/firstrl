import numpy as np # type: ignore
from tcod.console import Console

import tile_types


class GameMap:
    def __init__(self, width: int, height: int): # Takes width and height and assigns them in one line
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F") # Fill self.tiles array with wall tiles (to be carved out later)

    def in_bounds(self, x: int, y: int) -> bool: # Returns true as long as the player is within the map boundary
        """Return True if x and y are inside of the bounds of this map"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def render(self, console: Console) -> None: # Renders the map with the tiles.rgb method
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]