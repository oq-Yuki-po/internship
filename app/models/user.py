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
    ip : str
        user ip address
    machine_name : str
        user machine name
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), unique=True, nullable=False, comment='user name')
    ip = Column(String(39), unique=True, nullable=False, comment='ip address')
    machine_name = Column(String(40), unique=True, nullable=False, comment='machine name')

    def __init__(self,
                 name: str,
                 ip: str,
                 machine_name: str,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:
        """
        Parameters
        ----------
        name : str
            user name
        ip : str
            user ip address
        machine_name : str
            user machine name
        created_at : Optional[datetime], optional
            created datetime, by default None
        updated_at : Optional[datetime], optional
            updated datetime, by default None
        """

        self.name = name
        self.ip = ip
        self.machine_name = machine_name
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"<UserModel(name={self.name}) ip_address={self.ip} machine_name={self.machine_name}>)"

    @classmethod
    def save(cls, user: User) -> int:
        """
        save user

        fetch user by name, ip, machine_name
        if user is not exist, save user
        if user is exist, return user id

        Parameters
        ----------
        user : User
            user

        Returns
        -------
        int
            saved user id
        """

        if (user_model := cls.fetch_by_name_ip_machine_name(user.name, user.ip, user.machine_name)) is None:
            # if user is not exist, save user
            saved_user = cls(name=user.name, ip=user.ip, machine_name=user.machine_name)
            session.add(saved_user)
            session.flush()
            return saved_user.id
        return user_model.id

    @classmethod
    def fetch_by_name_ip_machine_name(cls, name: str, ip: str, machine_name: str) -> Optional[UserModel]:
        """
        fetch user by name, ip, machine_name

        if user is not exist, return None
        if user is exist, return user id

        Parameters
        ----------
        name : str
            user name
        ip : str
            user ip address
        machine_name : str
            user machine name

        Returns
        -------
        Optional[UserModel]
            fetched user
        """

        stmt = select(cls.id).where(cls.name == name
                                    and cls.ip == ip
                                    and machine_name == machine_name)

        """SQL
        SELECT users.id AS users_id
        FROM users
        WHERE users.name = :name_1
            AND users.ip = :ip_1
            AND users.machine_name = :machine_name_1
        """

        fetch_result = session.execute(stmt).one_or_none()

        return fetch_result


if __name__ == "__main__":
    BaseModel.metadata.create_all(bind=Engine)
