from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np # type: ignore
from tcod.console import Console

from entity import Actor
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    def __init__(
            self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F") # Fill self.tiles array with wall tiles (to be carved out later)

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        ) # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        ) # Tiles the player has seen before

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this map's living actors"""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    # Iterate through all entities, and if one is found that blocks movement and occupies given location_x and location_y coordinates, return the Entity; otherwise, return None
    def get_blocking_entity_at_location(
            self, location_x: int, location_y: int,
        ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity

        return None        

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
            
        return None

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
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select( # np.select replaces just setting tiles to "dark" with conditional tile drawing
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        for entity in self.entities:
            # Only print entities that are in the FOV
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)