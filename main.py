#!/usr/bin/env python3
import tcod

# Import functions from engine.py, entity,py, and input_handlers.py
from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


def main() -> None:
    # Define variables for the screen size and map size (smaller than screen to make room for HUD)
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    # Tell TCOD which font to use (loaded from file)
    tileset= tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler() # Create an instance of the EventHandler class, used to receive and process events

    # Use Entity class to initialize player and NPC
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player} # Set that will eventually hold all entities on the map

    game_map = GameMap(map_width, map_height)
    
    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

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
            engine.render(console=root_console, context=context)
 
            events = tcod.event.wait()

            engine.handle_events(events)

            
# Only run the main function when we explicitly run the script
if __name__ == "__main__":
    main()