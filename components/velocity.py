from ecs_core import Component

class VelocityComponent(Component):
    """
    Represents the velocity of an entity.
    """
    def __init__(self, vx: float = 0.0, vy: float = 0.0):
        self.vx = vx  # Velocity in x-direction (pixels per second)
        self.vy = vy  # Velocity in y-direction (pixels per second)