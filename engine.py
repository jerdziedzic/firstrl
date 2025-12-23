from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import EventHandler

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, player: Entity):
        self.entities = entities # Takes a set of entities that must be unique (which is why a list can't be used here)
        self.event_handler = event_handler # Same event handler from main.py; handles events
        self.player = player # Player entity; we have a separate reference outside of entities for ease of access (since we'll work with it a lot)

    # Basically same event handler we originally added to main.py
    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            if isinstance(action, MovementAction):
                self.player.move(dx=action.dx, dy=action.dy)

            elif isinstance(action, EscapeAction):
                raise SystemExit()

    # Draws the screen by iterating through entities and printing each, presenting context, clearing console            
    def render(self, console: Console, context: Context) -> None:
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()