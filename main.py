#!/usr/bin/env python3
import traceback

import tcod

# Import functions from engine.py, entity,py, and input_handlers.py
import color
import exceptions
import input_handlers
import setup_game


def main() -> None:
    screen_width = 80
    screen_height = 50

    # Tell TCOD which font to use (loaded from file)
    tileset= tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

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
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception: # Handle exceptions in game
                    traceback.print_exc() # Print error to stderr
                    # Then print the error to the message log
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit: # Save and quit
            # TODO: Add the save function here
            raise
        except BaseException: # Save on any other unexpected exceptions
            # TODO: Add the save function here
            raise
            
# Only run the main function when we explicitly run the script
if __name__ == "__main__":
    main()