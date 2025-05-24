from typing import Dict, List, Type, TypeVar, Optional, Set
from .entity import EntityManager
from .component import Component
from .system import System
from utils import logger as log # Assuming your logger is accessible

T = TypeVar('T', bound=Component)
S = TypeVar('S', bound=System)

EntityID = int

class Scene:
    def __init__(self):
        self.entity_manager = EntityManager()
        self.component_managers: Dict[Type[Component], Dict[EntityID, Component]] = {}
        self.systems: List[System] = []
        self.entities_to_destroy: Set[EntityID] = set()

    def create_entity(self) -> EntityID:
        return self.entity_manager.create_entity()

    def destroy_entity(self, entity_id: EntityID):
        """Marks an entity for destruction at the end of the current update cycle."""
        if entity_id in self.entity_manager.entities:
            self.entities_to_destroy.add(entity_id)

    def _process_destroyed_entities(self):
        for entity_id in self.entities_to_destroy:
            if entity_id in self.entity_manager.entities: # Check if not already processed
                for component_type in list(self.component_managers.keys()): # list() for safe iteration
                    if entity_id in self.component_managers[component_type]:
                        del self.component_managers[component_type][entity_id]
                self.entity_manager.destroy_entity(entity_id)
                log.debug(f"Scene: Destroyed entity {entity_id} and its components.")
        self.entities_to_destroy.clear()

    def add_component(self, entity_id: EntityID, component_instance: T):
        component_type = type(component_instance)
        if component_type not in self.component_managers:
            self.component_managers[component_type] = {}
        self.component_managers[component_type][entity_id] = component_instance
        log.debug(f"Scene: Added {component_type.__name__} to entity {entity_id}")

    def get_component(self, entity_id: EntityID, component_type: Type[T]) -> Optional[T]:
        if component_type in self.component_managers:
            return self.component_managers[component_type].get(entity_id)
        return None

    def remove_component(self, entity_id: EntityID, component_type: Type[Component]):
        if component_type in self.component_managers:
            if entity_id in self.component_managers[component_type]:
                del self.component_managers[component_type][entity_id]
                log.debug(f"Scene: Removed {component_type.__name__} from entity {entity_id}")
                if not self.component_managers[component_type]: # Clean up empty manager
                    del self.component_managers[component_type]

    def get_entities_with_components(self, *component_types: Type[Component]) -> List[EntityID]:
        if not component_types:
            return list(self.entity_manager.entities)

        # Start with entities having the first component type
        base_component_type = component_types[0]
        if base_component_type not in self.component_managers:
            return []

        candidate_entities = set(self.component_managers[base_component_type].keys())

        # Filter by subsequent component types
        for comp_type in component_types[1:]:
            if comp_type not in self.component_managers:
                return [] # If any component type is missing, no entities can match
            candidate_entities.intersection_update(self.component_managers[comp_type].keys())
            if not candidate_entities: # Early exit if intersection is empty
                return []

        return list(candidate_entities)

    def add_system(self, system_instance: S):
        system_instance.scene = self # Give system a reference to the scene
        self.systems.append(system_instance)
        log.info(f"Scene: Added system {type(system_instance).__name__}")

    def update(self, dt: float):
        for system in self.systems:
            system.update(dt)
        self._process_destroyed_entities() # Clean up entities marked for destruction
