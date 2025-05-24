from ecs_core.system import System
from components.transform import TransformComponent
from components import VelocityComponent
from components.renderable import RenderableComponent # Optional, for marking dirty
from utils import logger as log

class MovementSystem(System):
    """
    Updates entity positions based on their velocity.
    """
    def __init__(self):
        super().__init__()
        log.info("MovementSystem: Initialized.")

    def update(self, dt: float):
        entities = self.scene.get_entities_with_components(
            TransformComponent,
            VelocityComponent
        )

        for entity_id in entities:
            transform = self.scene.get_component(entity_id, TransformComponent)
            velocity = self.scene.get_component(entity_id, VelocityComponent)

            if transform and velocity and (velocity.vx != 0 or velocity.vy != 0):
                transform.x += velocity.vx * dt
                transform.y += velocity.vy * dt
                log.debug(f"MovementSystem: Entity {entity_id} moved to ({transform.x:.2f}, {transform.y:.2f}) with velocity ({velocity.vx:.2f}, {velocity.vy:.2f})")
                renderable = self.scene.get_component(entity_id, RenderableComponent)
                if renderable:
                    renderable.is_dirty = True
