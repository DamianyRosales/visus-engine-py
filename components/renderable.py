from ecs_core.component import Component
from typing import Any, Optional

# https://learn.microsoft.com/en-us/office/vba/api/office.msoautoshapetype
MSO_SHAPE_RECTANGLE = 1
MSO_SHAPE_OVAL = 9
MSO_SHAPE_ROUNDED_RECTANGLE = 5

class RenderableComponent(Component):
    def __init__(self, shape_type: int = MSO_SHAPE_RECTANGLE, 
                 color_rgb: int = 0x000000, # Black by default (BGR)
                 text: Optional[str] = None,
                 font_size: int = 18,
                 z_order: int = 0, # Higher numbers are more on top
                 visible: bool = True):
        self.shape_type = shape_type
        self.color_rgb = color_rgb # e.g., 0x0000FF for red (BGR)
        self.text = text
        self.font_size = font_size
        self.z_order = z_order # For ZOrder method
        self.visible = visible
        self.ppt_shape_object: Optional[Any] = None # To store the actual pywin32 shape object
        self.is_dirty = True # Flag to indicate if the shape needs update