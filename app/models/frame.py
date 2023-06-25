from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, String, select
from sqlalchemy.orm import relationship

from app.models import BaseModel, Engine, UserModel, session


class FrameModel(BaseModel):
    """
    FrameModel

    Attributes
    ----------
    id : int
        frame id
    frame_create_time : str
        frame create time
    user_id : int
        user id
    """
    __tablename__ = 'frames'
    id = Column(Integer, primary_key=True, autoincrement=True)
    frame_create_time = Column(String(19), unique=True, nullable=False, comment='frame create time')
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=False, comment='user id')

    user = relationship(UserModel, backref='frames')

    def __init__(self,
                 frame_create_time: str,
                 user_id: Optional[int] = None,
                 user: Optional[UserModel] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:
        """
        Parameters
        ----------
        frame_create_time : str
            frame create time
        user_id : int
            user id
        created_at : Optional[datetime], optional
            created datetime, by default None
        updated_at : Optional[datetime], optional
            updated datetime, by default None
        """

        self.frame_create_time = frame_create_time

        if user_id is not None:
            self.user_id = user_id
        elif user is not None:
            self.user = user
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"<FrameModel(frame_create_time={self.frame_create_time}, user_id={self.user_id})>"

    @classmethod
    def save(cls, user_id: int, frame_create_time: str) -> int:
        """
        save frame

        Parameters
        ----------
        user_id : int
            user id
        frame_create_time : str
            frame create time

        Returns
        -------
        int
            frame id
        """

        frame = cls(frame_create_time=frame_create_time, user_id=user_id)
        session.add(frame)
        session.flush()
        return frame.id
