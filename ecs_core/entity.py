import itertools

class EntityManager:
    def __init__(self):
        self.next_entity_id = itertools.count()
        self.entities = set()

    def create_entity(self) -> int:
        entity_id = next(self.next_entity_id)
        self.entities.add(entity_id)
        return entity_id

    def destroy_entity(self, entity_id: int):
        if entity_id in self.entities:
            self.entities.remove(entity_id)
        # Note: Components associated with this entity will need to be cleaned up by the Scene/ComponentManager
