from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, select
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models import BaseModel, UserModel, UserSessionModel, session


class FrameModel(BaseModel):
    """
    FrameModel

    Attributes
    ----------
    id : int
        frame id
    frame_create_time : str
        frame create time
    user_session_id : int
        user session id
    user_session : UserSessionModel
        user session
    """
    __tablename__ = 'frames'
    id = Column(Integer, primary_key=True, autoincrement=True)
    frame_create_time = Column(DateTime, nullable=False, comment='frame create time')
    user_session_id = Column(Integer, ForeignKey(UserSessionModel.id), nullable=False, comment='user session id')

    user_session = relationship(UserSessionModel, backref='frames')

    def __init__(self,
                 frame_create_time: str,
                 user_session_id: Optional[int] = None,
                 user_session: Optional[UserSessionModel] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:
        """
        Parameters
        ----------
        frame_create_time : str
            frame create time
        user_id : Optional[int], optional
            user id, by default None
        user : Optional[UserModel], optional
            user, by default None
        created_at : Optional[datetime], optional
            created datetime, by default None
        updated_at : Optional[datetime], optional
            updated datetime, by default None
        """

        self.frame_create_time = frame_create_time

        if user_session_id is not None:
            self.user_session_id = user_session_id
        elif user_session is not None:
            self.user_session = user_session
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"< FrameModel(frame_create_time={self.frame_create_time}, user_session_id={self.user_session_id}) >"

    @ classmethod
    def save(cls, frame: FrameModel) -> int:
        """
        save frame

        Parameters
        ----------
        frame : FrameModel
            frame

        Returns
        -------
        int
            frame id
        """

        if (frame_model := cls.fetch_by_frame_create_time_user_session_id(frame.frame_create_time,
                                                                          frame.user_session_id)) is None:
            frame = cls(frame_create_time=frame.frame_create_time, user_session_id=frame.user_session_id)
            session.add(frame)
            session.flush()
            return frame.id
        return frame_model.id

    @classmethod
    def fetch_by_frame_create_time_user_session_id(cls,
                                                   frame_create_time: str,
                                                   user_session_id: int) -> Optional[FrameModel]:
        """
        fetch frame by frame create time and user session id

        Parameters
        ----------
        frame_create_time : str
            frame create time
        user_session_id : int
            user session id

        Returns
        -------
        Optional[FrameModel]
            frame
        """

        stmt = select(cls.id).where(cls.frame_create_time == frame_create_time
                                    and cls.user_session_id == user_session_id)

        """SQL
        SELECT frames.id
        FROM frames
        WHERE frames.frame_create_time = %(frame_create_time_1) s
            AND frames.user_session_id = %(user_session_id_1) s
        """

        fetch_result = session.execute(stmt).one_or_none()

        return fetch_result

    @classmethod
    def fetch_all_user_session(cls) -> list[tuple[int, int, str, str, str, str]]:
        """
        fetch all user sessions and frames start time and end time

        Returns
        -------
        list[tuple[int, int, str, str, str, str]]
            user sessions and frames start time and end time
        """
        stmt = select(UserModel.id,
                      UserSessionModel.session_id,
                      UserModel.name,
                      UserModel.machine_name,
                      func.to_char(func.min(cls.frame_create_time),  # pylint: disable=not-callable
                                   'YYYY-MM-DD HH24:MI:SS').label('start_time'),
                      func.to_char(func.max(cls.frame_create_time),  # pylint: disable=not-callable
                                   'YYYY-MM-DD HH24:MI:SS').label('end_time')) \
            .join(UserSessionModel, UserSessionModel.user_id == UserModel.id)\
            .join(cls, cls.user_session_id == UserSessionModel.id)\
            .group_by(UserModel.id, UserSessionModel.session_id, UserModel.name, UserModel.machine_name)\
            .order_by(UserModel.name)

        """SQL
        SELECT users.id,
            user_sessions.session_id,
            users.name,
            users.machine_name,
            to_char(min(frames.frame_create_time), 'YYYY-MM-DD HH24:MI:SS') AS start_time,
            to_char(max(frames.frame_create_time), 'YYYY-MM-DD HH24:MI:SS') AS end_time
        FROM users
        JOIN user_sessions ON user_sessions.user_id = users.id
        JOIN frames ON frames.user_session_id = user_sessions.id
        GROUP BY users.id,
            user_sessions.session_id,
            users.name,
            users.machine_name
        ORDER BY users.name
        """

        fetch_result = session.execute(stmt).all()
        return fetch_result

    @classmethod
    def fetch_frame_by_session_id_frame_no(cls, session_id: str, frame_no: int):
        """
        fetch frame by session id and frame no

        Parameters
        ----------
        session_id : str
            session id of user which is uuid
        frame_no : int
            frame no
        """

        stmt = select(FrameModel.id,
                      func.to_char(cls.frame_create_time,  # pylint: disable=not-callable
                                   'YYYY-MM-DD HH24:MI:SS').label('frame_create_time')).\
            join(UserSessionModel, cls.user_session_id == UserSessionModel.id).\
            where(UserSessionModel.session_id == session_id).\
            order_by(cls.frame_create_time).\
            limit(1).\
            offset(frame_no - 1)

        """SQL
        SELECT frames.id,
            to_char(frames.frame_create_time, 'YYYY-MM-DD HH24:MI:SS') AS frame_create_time
        FROM frames
        JOIN user_sessions ON frames.user_session_id = user_sessions.id
        WHERE user_sessions.session_id = %(session_id_1) s
        ORDER BY frames.frame_create_time
        LIMIT %(param_1) s
        OFFSET %(param_2) s
        """

        fetch_result = session.execute(stmt).one()

        return fetch_result
