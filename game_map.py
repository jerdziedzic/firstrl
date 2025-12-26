import numpy as np # type: ignore
from tcod.console import Console

import tile_types


class GameMap:
    def __init__(self, width: int, height: int): # Takes width and height and assigns them in one line
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F") # Fill self.tiles array with wall tiles (to be carved out later)

        self.visible = np.full((width, height), fill_value=False, order="F") # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F") # Tiles the player has seen before

    def in_bounds(self, x: int, y: int) -> bool: # Returns true as long as the player is within the map boundary
        """Return True if x and y are inside of the bounds of this map"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def render(self, console: Console) -> None: # Renders the map with the tiles.rgb method
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select( # np.select replaces just setting tiles to "dark" with conditional tile drawing
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )