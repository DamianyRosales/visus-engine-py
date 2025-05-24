import time, keyboard
from COM.com_client import Client
from ecs_core import Scene
from components import TransformComponent, UserControlledComponent, VelocityComponent
from components.renderable import RenderableComponent, MSO_SHAPE_RECTANGLE, MSO_SHAPE_OVAL
from systems import RenderingSystem, InputSystem, MovementSystem
from utils import logger as log

# Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
TARGET_FPS = 30
FRAME_TIME = 1.0 / TARGET_FPS

def game_main():
    log.info("Starting PowerPoint Game Engine...")

    com_client = Client(dispatch="PowerPoint.Application", visible=True)
    ppt_app = com_client.get_app()

    try:
        if ppt_app.Presentations.Count == 0:
            presentation = ppt_app.Presentations.Add()
        else:
            presentation = ppt_app.ActivePresentation 

        if presentation.Slides.Count == 0:
            slide = presentation.Slides.Add(1, 12) # 12 = ppLayoutBlank
        else:
            slide = presentation.Slides(1)
        
        """
        Optional: Set slide size (if not default)
        presentation.PageSetup.SlideWidth = SCREEN_WIDTH
        presentation.PageSetup.SlideHeight = SCREEN_HEIGHT
        """

        log.info(f"Using slide: {slide.Name}")

        # 3. Initialize ECS Scene
        scene = Scene()

        # 4. Create Systems
        rendering_sys = RenderingSystem(powerpoint_slide_object=slide)
        input_sys = InputSystem()
        movement_sys = MovementSystem()

        # 5. Add Systems to Scene (order can matter)
        scene.add_system(input_sys)
        scene.add_system(movement_sys)
        scene.add_system(rendering_sys)


        # 6. Create Game Entities
        player_entity = scene.create_entity()
        scene.add_component(player_entity, TransformComponent(x=50, y=50, width=50, height=50))
        scene.add_component(player_entity, RenderableComponent(shape_type=MSO_SHAPE_OVAL, color_rgb=0x00FF00, text="Player")) # Green
        scene.add_component(player_entity, UserControlledComponent(movement_speed=200))
        scene.add_component(player_entity, VelocityComponent()) # Add velocity for movement system

        box_entity = scene.create_entity()
        scene.add_component(box_entity, TransformComponent(x=200, y=100, width=80, height=120, rotation=15))
        scene.add_component(box_entity, RenderableComponent(shape_type=MSO_SHAPE_RECTANGLE, color_rgb=0x0000FF, text="Hello!")) # Red

        # 7. Game Loop
        running = True
        last_time = time.perf_counter()

        log.info("Starting game loop...")
        while running:
            """
             TODO:
             import pythoncom
             pythoncom.PumpWaitingMessages()
            """
            current_time = time.perf_counter()
            dt = current_time - last_time
            last_time = current_time

            try:

                if keyboard.is_pressed('esc'):
                    log.info("Escape key pressed. Exiting game loop.")
                    running = False

            except Exception as e:
                log.warn(f"Could not check for escape key via 'keyboard' lib: {e}")


            # --- Update Game Logic ---
            scene.update(dt) # This will call update on all systems

            # --- Frame Limiting ---
            sleep_time = FRAME_TIME - (time.perf_counter() - current_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

        log.info("Game loop finished.")

    except Exception as e:
        log.exception(f"An error occurred during the game: {e}")
    finally:
        log.info("Cleaning up and quitting PowerPoint...")
        """
        for entity_id in scene.get_entities_with_components(RenderableComponent):
            renderable = scene.get_component(entity_id, RenderableComponent)
            if renderable and renderable.ppt_shape_object:
                try:
                    renderable.ppt_shape_object.Delete()
                except: pass
        """
        com_client.quit()
        log.info("Cleanup complete. Exiting application.")


if __name__ == "__main__":

    game_main()

