from typing import Optional

from sqlalchemy.orm import Session

from seedwork.domain import Entity
from seedwork.domain.entity import EntityId
from seedwork.domain.repository.generic import GenericRepository

__all__ = ['SQLAlchemyGenericRepository']


class SQLAlchemyGenericRepository(GenericRepository[Entity]):
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def get(self, entity_id: EntityId) -> Optional[Entity]:
        return self.session.get(Entity, entity_id)

    def create(self, entity: Entity) -> Entity:
        self.session.add(entity)
        return entity

    def update(self, entity_id: EntityId, entity: Entity) -> Optional[Entity]:
        self.session.add(entity)
        return entity

    def delete(self, entity_id: EntityId) -> None:
        entity = self.get(entity_id)
        if entity:
            self.session.delete(entity)

    def commit(self) -> None:
        self.session.commit()
