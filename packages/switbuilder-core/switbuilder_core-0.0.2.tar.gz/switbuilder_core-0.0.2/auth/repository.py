from fastapi import HTTPException
from sqlalchemy.orm import Session

from auth.models import App, User


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


class UserRepository(RepositoryBase):
    def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_or_create(self, **kwargs):
        user_or_null = self.get_by_swit_id(kwargs.get('swit_id', ''))
        if user_or_null is None:
            user_or_null = self.create(**kwargs)
        return user_or_null

    def get_by_swit_id(self, swit_id: str) -> User | None:
        return self.session.query(User).filter(User.swit_id == swit_id).first()

    def update(
            self,
            swit_id: str,
            access_token: str = "",
            refresh_token: str = ""
    ) -> User:
        user = self.get_by_swit_id(swit_id=swit_id)

        if access_token:
            user.access_token = access_token

        if refresh_token:
            user.refresh_token = refresh_token

        self.session.commit()
        return user

    def delete(self, swit_id: str) -> None:
        user = self.get_by_swit_id(swit_id)
        if user is None:
            return

        self.session.delete(user)
        self.session.commit()
