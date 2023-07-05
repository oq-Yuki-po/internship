from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models import BaseModel, FrameModel, session
from app.schemas.requests.sensors import RequestProcessSensor


class ProcessSensorModel(BaseModel):
    """
    ProcessSensorModel

    Attributes
    ----------
    id : int
        ip port
    file_path : str
        file path
    process_name : str
        process name
    process_id : int
        process id
    started_at : datetime
        started at
    frame_id : int
        frame id
    frame : FrameModel
        frame
    """
    __tablename__ = 'process_sensors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String(255), nullable=False, comment='file path')
    process_name = Column(String(255), nullable=False, comment='process name')
    process_id = Column(Integer, nullable=False, comment='process id')
    started_at = Column(DateTime, nullable=False, comment='started at')
    frame_id = Column(Integer, ForeignKey(FrameModel.id), nullable=False, comment='frame id')

    frame = relationship(FrameModel, backref='process_sensors')

    def __init__(self,
                 file_path: str,
                 process_name: str,
                 process_id: int,
                 started_at: str,
                 frame_id: Optional[int] = None,
                 frame: Optional[FrameModel] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:
        """
        Parameters
        ----------
        frame_id : Optional[int], optional
            frame id, by default None
        frame : Optional[FrameModel], optional
            frame, by default None
        created_at : Optional[datetime], optional
            created datetime, by default None
        updated_at : Optional[datetime], optional
            updated datetime, by default None
        """
        self.file_path = file_path
        self.process_name = process_name
        self.process_id = process_id
        self.started_at = started_at
        if frame_id is not None:
            self.frame_id = frame_id
        elif frame is not None:
            self.frame = frame
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"<ProcessSensorModel(id={self.id}, " \
            f"file_path={self.file_path}, " \
            f"process_name={self.process_name}, " \
            f"process_id={self.process_id}, " \
            f"started_at={self.started_at}, " \
            f"frame_id={self.frame_id}, " \
            f"created_at={self.created_at}, " \
            f"updated_at={self.updated_at})>"

    @classmethod
    def save(cls, request_process_sensors: list[RequestProcessSensor], frame_id: int) -> None:
        """Save process sensors.

        Parameters
        ----------
        request_process_sensors : list[RequestProcessSensor]
            request process sensors
        frame_id : int
            frame id
        """
        process_sensors = []
        for request_process_sensor in request_process_sensors:
            process_sensors.append(cls(
                file_path=request_process_sensor.file_path,
                process_name=request_process_sensor.process_name,
                process_id=request_process_sensor.process_id,
                started_at=request_process_sensor.started_at,
                frame_id=frame_id
            ))
        session.add_all(process_sensors)
