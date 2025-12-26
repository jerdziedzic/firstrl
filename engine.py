from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap, player: Entity):
        self.entities = entities # Takes a set of entities that must be unique (which is why a list can't be used here)
        self.event_handler = event_handler # Same event handler from main.py; handles events
        self.game_map = game_map
        self.player = player # Player entity; we have a separate reference outside of entities for ease of access (since we'll work with it a lot)
        self.update_fov()

    # Basically same event handler we originally added to main.py
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov() # Update the FOV before the player's next action

    def update_fov(self) -> None:
        """Recompute the visible area based on the player's point of view"""
        self.game_map.visible[:] = compute_fov( # Set the game_map's visible tiles equal to result of compute_fov
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored"
        self.game_map.explored |= self.game_map.visible


    # Draws the screen by iterating through entities and printing each, presenting context, clearing console            
    def render(self, console: Console, context: Context) -> None:

        self.game_map.render(console)

        for entity in self.entities:
            # Only print entities that are in the FOV
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()