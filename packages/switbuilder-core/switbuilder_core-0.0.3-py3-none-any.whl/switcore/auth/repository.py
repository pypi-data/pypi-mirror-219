from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.auth.models import App


class RepositoryBase:
    def __init__(self, session: Session):
        self.session = session


class AppRepository(RepositoryBase):
    def create(self, **kwargs) -> App:
        token = App(**kwargs)
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)
        return token

    def get_by_id(self, id: int) -> App:
        token = self.session.query(App).get(id)
        if token is None:
            raise HTTPException(status_code=404, detail="Token not found")
        return token

    def get_all(self) -> list[App]:
        return self.session.query(App).all()

    def delete(self, id: int) -> None:
        token = self.get_by_id(id)
        self.session.delete(token)
        self.session.commit()

