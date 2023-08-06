from sqlalchemy.orm import Session

__all__ = ['SQLAlchemyRepository']


class SQLAlchemyRepository:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
