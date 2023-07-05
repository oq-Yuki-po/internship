from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import UUID, Column, ForeignKey, Integer, select
from sqlalchemy.orm import relationship

from app.models import BaseModel, UserModel, session


class UserSessionModel(BaseModel):
    """
    UserSessionModel

    Attributes
    ----------
    id : int
        user session id
    session_id : UUID
        session id which is uuid.
        represents the session between when the user opens and closes the PC.
    user_id : int
        user id
    """
    __tablename__ = 'user_sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), unique=True, nullable=False, comment='session id')
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=False, comment='user id')

    user = relationship(UserModel, backref='user_sessions')

    def __init__(self,
                 session_id: UUID,
                 user_id: Optional[int] = None,
                 user: Optional[UserModel] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:
        """
        Parameters
        ----------
        session_id : UUID
            session id which is uuid
        user_id : int
            user id
        created_at : Optional[datetime], optional
            created datetime, by default None
        updated_at : Optional[datetime], optional
            updated datetime, by default None
        """

        self.session_id = session_id

        if user_id is not None:
            self.user_id = user_id
        elif user is not None:
            self.user = user
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"<UserSessionModel(id={self.id}, session_id={self.session_id}, user_id={self.user_id})>"

    @classmethod
    def save(cls, user_session: UserSessionModel) -> int:
        """
        save user session

        Returns
        -------
        int
            user session id
        """

        if (user_session_model := cls.fetch_by_session_id(user_session.session_id)) is None:
            session.add(user_session)
            session.flush()
            return user_session.id
        return user_session_model.id

    @classmethod
    def fetch_by_session_id(cls, session_id: UUID) -> Optional[UserSessionModel]:
        """
        fetch user session by session id
        if not found, return None

        Parameters
        ----------
        session_id : UUID
            session id

        Returns
        -------
        Optional[UserSessionModel]
            user session

        """

        stmt = select(cls.id).where(cls.session_id == session_id)

        """SQL
        SELECT
            session_id
        FROM
            user_sessions
        WHERE
            session_id = :session_id_1
        """

        fetch_result = session.execute(stmt).one_or_none()

        return fetch_result
