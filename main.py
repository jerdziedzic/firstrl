#!/usr/bin/env python3
import tcod

# Import functions from actions.py, entity,py, and input_handlers.py
from actions import EscapeAction, MovementAction
from entity import Entity
from input_handlers import EventHandler


def main() -> None:
    # Define variables for the screen size
    screen_width = 80
    screen_height = 50

    # Tell TCOD which font to use (loaded from file)
    tileset= tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler() # Create an instance of the EventHandler class, used to receive and process events

    # Use Entity class to initialize player and NPC
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player} # Set that will eventually hold all entities on the map

    # Create the screen and pass size parameters, tileset, title, and vsync boolean
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F") # Creates console to draw to; F flips y,x to x,y
        # Start of main game loop
        while True:
            root_console.print(x=player.x, y=player.y, string=player.char, fg=player.color) # Pass player starting coordinates, character, and color

            context.present(root_console)

            root_console.clear() # Clear the console after drawing to it (to eliminate leftover drawn characters from movement)

            # Allows us to quit by clicking upper-right X
            for event in tcod.event.wait():

                # Send an event to the event handler's dispatch method (which sends an event to its proper place)
                action = event_handler.dispatch(event)

                if action is None: # If no key is pressed or the pressed key is unrecognized, skip over the rest of the loop
                    continue

                # Add -1, 0, or +1 to player_x and/or player_y to move the character around
                if isinstance(action, MovementAction):
                    player.move(dx=action.dx, dy=action.dy) # Entity class handles movement

                # If Esc is pressed, exit the program
                elif isinstance(action, EscapeAction):
                    raise SystemExit()


# Only run the main function when we explicitly run the script
if __name__ == "__main__":
    main()