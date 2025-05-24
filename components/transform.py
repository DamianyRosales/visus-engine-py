from ecs_core.component import Component

class TransformComponent(Component):
    def __init__(self, x: float = 0, y: float = 0, width: float = 100, height: float = 100, rotation: float = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation # In degrees