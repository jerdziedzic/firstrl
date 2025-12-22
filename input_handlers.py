from typing import Optional # Part of Python's optional type hinting system; Optional means this can be "none"

import tcod.event # Import only the TCOD event system

from actions import Action, EscapeAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]): # Import the Action class and its subclasses
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]: # Called when we click upper-right X
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]: # Receive a keypress and return either an Action subclass or None
        action: Optional[Action] = None # action is a variable that holds whatever subclass we assign it to (or None)

        key = event.sym # key variable holds the actual keypress (no modifiers like Shift or Alt)

        # Execute actions based on keypress for movement and Esc
        if key == tcod.event.K_UP:
            action == MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action == MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action == MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action == MovementAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action == EscapeAction()

        # No valid key was pressed
        return action