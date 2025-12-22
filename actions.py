# Define generic class for actions
class Action:
    pass

# Subclass of Action; defines what happens when we press Esc
class EscapeAction(Action):
    pass

# Subclass of Action; defines both the fact that we're trying to move and what direction
class MovementAction(Action):
    def _init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy