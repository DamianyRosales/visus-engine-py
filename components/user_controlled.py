from ecs_core.component import Component

class UserControlledComponent(Component):
    
    def __init__(self, movement_speed: float = 150.0):
        self.movement_speed = movement_speed