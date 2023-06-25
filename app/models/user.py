from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, select

from app.models import BaseModel, Engine, session
from app.schemas.requests import User


class UserModel(BaseModel):
    """
    UserModel

    Attributes
    ----------
    id : int
        user id
    name : str
        user name
    ip_address : str
        user ip address
    machine_name : str
        user machine name
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), unique=True, nullable=False, comment='user name')
    ip_address = Column(String(39), unique=True, nullable=False, comment='ip address')
    machine_name = Column(String(40), unique=True, nullable=False, comment='machine name')

    def __init__(self,
                 name: str,
                 ip_address: str,
                 machine_name: str,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:
        """
        Parameters
        ----------
        name : str
            user name
        ip_address : str
            user ip address
        machine_name : str
            user machine name
        created_at : Optional[datetime], optional
            created datetime, by default None
        updated_at : Optional[datetime], optional
            updated datetime, by default None
        """

        self.name = name
        self.ip_address = ip_address
        self.machine_name = machine_name
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"<UserModel(name={self.name}) ip_address={self.ip_address} machine_name={self.machine_name}>)"

    @classmethod
    def save(cls, user: User) -> int:
        """
        save user

        Parameters
        ----------
        user : User
            user

        Returns
        -------
        int
            saved user id
        """

        if (user_model := cls.fetch_by_name(user.name)) is None:
            saved_user = cls(name=user.name, ip_address=user.ip_address, machine_name=user.machine_name)
            session.add(saved_user)
            session.flush()
            return saved_user.id
        return user_model.id

    @classmethod
    def fetch_by_name(cls, name: str) -> Optional[UserModel]:
        """
        fetch user by name

        Parameters
        ----------
        name : str
            user name
        """

        stmt = select(cls).where(cls.name == name)
        fetch_result = session.scalars(stmt).one_or_none()

        return fetch_result


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=Engine)
