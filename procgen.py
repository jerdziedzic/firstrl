from typing import Tuple

from game_map import GameMap
import tile_types

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int): # Takes x and y coordinates of top-left corner, computes bottom-right based on width and height
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + width

    @property
    def center(self) -> Tuple[int, int]: # Center acts as a read-only variable that describes x and y coordinates of a room (for later use)
        center_x = int ((self.x1 + self.x2) / 2)
        center_y = int ((self.y1 + self.y2) / 2)

        return center_x, center_y
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index"""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2) # The +1 covers cases where two rooms are created next to each other (wall needed)
    

def generate_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor

    return dungeon