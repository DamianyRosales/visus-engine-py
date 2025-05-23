from utils import logger as log

class Entity:
    
    def __init__(self,
        position_x=0, 
        position_y=0,
        max_health=100, 
        current_health=100,
    ):
        self.id = id(self)
        self.position_x = position_x
        self.position_y = position_y
        self.speed = 1
        self.max_health = max_health
        self.current_health = current_health
        self.is_alive = True
        self.hostile = False
    
    def set_position(self, position=[0,0]):
        self.position = position

    def set_current_health(self, health):
        if health > self.max_health:
            entity_details = {
                "id": self.id,
                "max_health": self.max_health,
                "current_health": self.current_health,
                "in_slide_entity": 1
            }
            log.warn(f'Trying to set health to a greater value({health}) than max health({self.max_health})')
            log.warn(f'Entity details: {entity_details}')
            self.current_health = health

    def get_current_health(self):
        return self.current_health