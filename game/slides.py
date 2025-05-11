from utils import logger as log

class Slides:
        
    def __init__(self, app):
        self._app = app
        self.__slides_collection = {}
        self.level_slide = 0
        self.render_slide = 1

    def get_slides_collection(self):
        return self.__slides_collection

    # Updates __slides_collection
    def update_slides_collection(self):
        try:
            collection = {}

            for slide in self._app.ActivePresentation.Slides:
                collection[slide.SlideId] = slide.SlideNumber
            
            self.__slides_collection = collection
        except Exception as error:
            log.error(f"Failed while getting slides collection", error)

    
    # Sets the slide to where a level design is in place 
    def set_level_slide(self, level_slide=None):
        try:
            if level_slide not in dict.values(self.__slides_collection):
                raise Exception(f"The level_slide provided({level_slide}) does not exist inside slides collection")
            
            self.level_slide = level_slide
        except Exception as error:
            log.error(f"Failed while set_level_slide()",error)
    
    
    # Sets the slide to where the level design will be rendered
    def set_render_slide(self, render_slide):
        self.render_slide = render_slide