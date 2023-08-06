from dataclasses import dataclass

from seedwork.domain.entity import Entity


@dataclass
class AggregateRoot(Entity):
    """Aggregate root base class.

    See Also:
        - https://martinfowler.com/bliki/DDD_Aggregate.html

    """
