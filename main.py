#!/usr/bin/env python3
import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler


def main() -> None:
    # Define variables for the screen size and player starting position
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2) # int ensures that this will not result in a float
    player_y = int(screen_height / 2)

    # Tell TCOD which font to use (loaded from file)
    tileset= tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

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
            root_console.print(x=player_x, y=player_y, string="@") # Tell root console to print @ at starting coordinates

            context.present(root_console)

            # Allows us to quit by clicking upper-right X
            for event in tcod.event.wait():

                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                elif isinstance(action, EscapeAction):
                    raise SystemExit()


# Only run the main function when we explicitly run the script
if __name__ == "__main__":
    main()