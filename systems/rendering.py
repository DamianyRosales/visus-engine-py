from ecs_core.system import System
from components.transform import TransformComponent
from components.renderable import RenderableComponent
from COM.com_client import Client # Your COM client
from utils import logger as log

# For ZOrder constants
# msoZOrderBringToFront = 0
# msoZOrderSendToBack = 1
# msoZOrderBringForward = 2
# msoZOrderSendBackward = 3
# msoZOrderBringInFrontOfText = 4 (Not usually for shapes)
# msoZOrderSendBehindText = 5 (Not usually for shapes)

class RenderingSystem(System):
    def __init__(self, powerpoint_slide_object):
        super().__init__()
        self.com_client = Client() # Get the singleton instance
        self.powerpoint_app = self.com_client.get_app()
        if not self.powerpoint_app:
            log.error("RenderingSystem: PowerPoint application not available!")
            raise RuntimeError("PowerPoint application not initialized.")

        self.slide = powerpoint_slide_object # Pass the target slide object here
        if not self.slide:
            log.error("RenderingSystem: PowerPoint slide object not provided!")
            raise ValueError("A valid PowerPoint slide object is required for the RenderingSystem.")

        log.info("RenderingSystem: Initialized.")

    def update(self, dt: float):
        entities_to_render = self.scene.get_entities_with_components(TransformComponent, RenderableComponent)

        """
        Sort by z_order for correct drawing order (optional, but good for complex scenes)
        This is more about creation order or explicit ZOrder calls if things overlap significantly
        entities_to_render.sort(key=lambda eid: self.scene.get_component(eid, RenderableComponent).z_order)
        """

        for entity_id in entities_to_render:
            transform = self.scene.get_component(entity_id, TransformComponent)
            renderable = self.scene.get_component(entity_id, RenderableComponent)

            if not transform or not renderable:
                continue

            if not renderable.visible:
                if renderable.ppt_shape_object:
                    try:
                        renderable.ppt_shape_object.Visible = False
                    except Exception as e:
                        log.error(f"RenderingSystem: Error hiding shape for entity {entity_id}: {e}")
                continue # Skip invisible objects

            # Create shape if it doesn't exist
            if renderable.ppt_shape_object is None:
                try:
                    log.debug(f"RenderingSystem: Creating shape for entity {entity_id}")
                    # AddShape(Type, Left, Top, Width, Height)
                    shape = self.slide.Shapes.AddShape(
                        renderable.shape_type,
                        transform.x,
                        transform.y,
                        transform.width,
                        transform.height
                    )
                    renderable.ppt_shape_object = shape
                    renderable.is_dirty = True # Mark dirty to apply all properties
                except Exception as e:
                    log.error(f"RenderingSystem: Failed to create shape for entity {entity_id}: {e}")
                    # Potentially remove the renderable component or mark entity for destruction
                    self.scene.remove_component(entity_id, RenderableComponent)
                    continue

            # Update existing shape if it's "dirty" or always (for simplicity now)
            # A more optimized way would be to only update if transform/renderable properties changed
            if renderable.ppt_shape_object and renderable.is_dirty: # or always update for now
                shape = renderable.ppt_shape_object
                try:
                    shape.Visible = True # Ensure it's visible if it was hidden
                    shape.Left = transform.x
                    shape.Top = transform.y
                    shape.Width = transform.width
                    shape.Height = transform.height
                    shape.Rotation = transform.rotation

                    # Fill color
                    shape.Fill.ForeColor.RGB = renderable.color_rgb
                    shape.Fill.Visible = True # msoTrue

                    # Line color (optional, default is usually black or none)
                    # shape.Line.ForeColor.RGB = 0x0000FF # Blue line
                    # shape.Line.Visible = True

                    if renderable.text is not None:
                        if shape.HasTextFrame:
                            shape.TextFrame.TextRange.Text = renderable.text
                            shape.TextFrame.TextRange.Font.Size = renderable.font_size
                            # shape.TextFrame.TextRange.Font.Color.RGB = 0xFFFFFF # White text

                    renderable.is_dirty = False # Reset dirty flag
                    log.debug(f"RenderingSystem: Updated shape for entity {entity_id}")
                except Exception as e:
                    log.error(f"RenderingSystem: Failed to update shape for entity {entity_id}: {e}")
                    """
                    If a COM error occurs (e.g., shape deleted manually in PPT),
                    nullify the reference so it can be recreated.
                    """
                    renderable.ppt_shape_object = None
                    renderable.is_dirty = True # Mark for recreation attempt next frame

        # Handle destroyed entities: remove their PowerPoint shapes
        for entity_id in self.scene.entities_to_destroy: # Check entities marked for destruction
            """
            Need to get the renderable component BEFORE it's removed by Scene._process_destroyed_entities
            This is a bit tricky. A better way might be for systems to react to "entity_destroyed" events.
            For now, will assume it can still be accessed it if we check before _process_destroyed_entities runs.
            This part needs careful thought on event ordering or storing ppt_shape_object temporarily.
            
            A temporary workaround: iterate all renderables and see if their entity is in entities_to_destroy
            This is inefficient.
            """

            all_render_entities = self.scene.get_entities_with_components(RenderableComponent)
            for rend_entity_id in all_render_entities:
                if rend_entity_id in self.scene.entities_to_destroy:
                    renderable_comp = self.scene.get_component(rend_entity_id, RenderableComponent)
                    if renderable_comp and renderable_comp.ppt_shape_object:
                        try:
                            log.debug(f"RenderingSystem: Deleting shape for destroyed entity {rend_entity_id}")
                            renderable_comp.ppt_shape_object.Delete()
                            renderable_comp.ppt_shape_object = None
                        except Exception as e:
                            log.error(f"RenderingSystem: Error deleting shape for entity {rend_entity_id}: {e}")
                            renderable_comp.ppt_shape_object = None # Ensure it's cleared
