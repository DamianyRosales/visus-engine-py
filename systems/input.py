from ecs_core.system import System
from components import UserControlledComponent, VelocityComponent
from utils import logger as log

try:
    import keyboard
    _KEYBOARD_LIB_AVAILABLE = True
except ImportError:
    log.warn("InputSystem: 'keyboard' library not found. Player movement will be disabled. Please install it using 'pip install keyboard'.")
    _KEYBOARD_LIB_AVAILABLE = False
except Exception as e:
    log.warn(f"InputSystem: 'keyboard' library failed to initialize (may need admin rights or specific environment setup): {e}. Player movement will be disabled.")
    _KEYBOARD_LIB_AVAILABLE = False

class InputSystem(System):
    def __init__(self):
        super().__init__()
        self._keyboard_active = _KEYBOARD_LIB_AVAILABLE
        if self._keyboard_active:
            log.info("InputSystem: Initialized. Listening for player input.")
        else:
            log.info("InputSystem: Initialized, but keyboard input is disabled due to missing or problematic 'keyboard' library.")

    def update(self, dt: float):
        if not self._keyboard_active:
            return

        # Get all entities that are player-controlled and have a velocity component
        entities = self.scene.get_entities_with_components(
            UserControlledComponent,
            VelocityComponent
        )

        for entity_id in entities:
            user_controlled = self.scene.get_component(entity_id, UserControlledComponent)
            velocity = self.scene.get_component(entity_id, VelocityComponent)

            if not (user_controlled and velocity):
                continue

            current_vx, current_vy = 0.0, 0.0
            speed = user_controlled.movement_speed

            try:
                if keyboard.is_pressed('a') or keyboard.is_pressed('a'):
                    current_vx -= speed
                if keyboard.is_pressed('d') or keyboard.is_pressed('d'):
                    current_vx += speed
                if keyboard.is_pressed('w') or keyboard.is_pressed('w'):
                    current_vy -= speed
                if keyboard.is_pressed('s') or keyboard.is_pressed('s'):
                    current_vy += speed
            except Exception as e:
                log.error(f"InputSystem: Error reading keyboard state: {e}. Disabling keyboard input for this session.")
                self._keyboard_active = False # Disable further checks to avoid spamming logs and errors.
                return # Stop processing input for this frame.

            # Update velocity component if it has changed
            if velocity.vx != current_vx or velocity.vy != current_vy:
                velocity.vx = current_vx
                velocity.vy = current_vy
                log.debug(f"InputSystem: Entity {entity_id} velocity set to ({velocity.vx:.2f}, {velocity.vy:.2f})")