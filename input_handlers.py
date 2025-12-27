from __future__ import annotations

from typing import Optional, TYPE_CHECKING # Part of Python's optional type hinting system; Optional means this can be "none"

import tcod.event # Import only the TCOD event system

from actions import Action, BumpAction, EscapeAction

if TYPE_CHECKING:
    from engine import Engine


class EventHandler(tcod.event.EventDispatch[Action]): # Import the Action class and its subclasses
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov() # Update the FOV before the player's next action

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]: # Called when we click upper-right X
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]: # Receive a keypress and return either an Action subclass or None
        action: Optional[Action] = None # action is a variable that holds whatever subclass we assign it to (or None)

        key = event.sym # key variable holds the actual keypress (no modifiers like Shift or Alt)

        player = self.engine.player

        # Execute actions based on keypress for movement and Esc
        if key == tcod.event.K_UP:
            action = BumpAction(player, dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = BumpAction(player, dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = BumpAction(player, dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = BumpAction(player, dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(player)

        # No valid key was pressed
        return action