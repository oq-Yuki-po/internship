from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models import BaseModel, FrameModel, session
from app.models.setting import metadata
from app.schemas.requests.sensors.drive import DriveType, RequestDriveSensor


class DriveSensorModel(BaseModel):
    """
    DriveSensorModel

    Attributes
    ----------
    id : int
        drive sensor id
    drive_letter : str
        drive letter
    drive_type : DriveType
        drive type
    volume_name : str
        volume name
    file_system : str
        file system
    all_space : str
        all space
    free_space : str
        free space
    frame_id : int
        frame id
    frame : FrameModel
        frame
    """
    __tablename__ = 'drive_sensors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    drive_letter = Column(String(1), nullable=False, comment='drive letter')
    drive_type = Column(Enum(DriveType, metadata=metadata), nullable=False, comment='drive type')
    volume_name = Column(String(255), nullable=False, comment='volume name')
    file_system = Column(String(255), nullable=False, comment='file system')
    all_space = Column(String(16), nullable=False, comment='all space')
    free_space = Column(String(16), nullable=False, comment='free space')
    frame_id = Column(Integer, ForeignKey(FrameModel.id), nullable=False, comment='frame id')

    frame = relationship(FrameModel, backref='drive_sensors')

    def __init__(self,
                 drive_letter: str,
                 drive_type: DriveType,
                 volume_name: str,
                 file_system: str,
                 all_space: str,
                 free_space: str,
                 frame_id: Optional[int] = None,
                 frame: Optional[FrameModel] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:
        """
        Parameters
        ----------
        drive_letter : str
            drive letter
        drive_type : DriveType
            drive type
        volume_name : str
            volume name
        file_system : str
            file system
        all_space : str
            all space
        free_space : str
            free space
        frame_id : Optional[int], optional
            frame id, by default None
        frame : Optional[FrameModel], optional
            frame, by default None
        created_at : Optional[datetime], optional
            created datetime, by default None
        updated_at : Optional[datetime], optional
            updated datetime, by default None
        """

        self.drive_letter = drive_letter
        self.drive_type = drive_type
        self.volume_name = volume_name
        self.file_system = file_system
        self.all_space = all_space
        self.free_space = free_space

        if frame_id is not None:
            self.frame_id = frame_id
        elif frame is not None:
            self.frame = frame
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"< DriveSensorModel id={self.id} drive_letter={self.drive_letter} drive_type={self.drive_type} "\
            f"volume_name={self.volume_name} file_system={self.file_system} all_space={self.all_space} "\
            f"free_space={self.free_space} frame_id={self.frame_id} " \
            f"created_at={self.created_at} updated_at={self.updated_at} >"

    @classmethod
    def save(cls, request_drive_sensors: list[RequestDriveSensor], frame_id: int) -> None:
        """Save drive sensors.

        Parameters
        ----------
        drive_sensors : list[RequestDriveSensor]
            drive sensors
        frame_id : int
            frame id
        """
        drive_sensors = []
        for request_drive_sensor in request_drive_sensors:
            drive_sensor_model = cls(
                drive_letter=request_drive_sensor.drive_letter,
                drive_type=request_drive_sensor.drive_type.value,
                volume_name=request_drive_sensor.volume_name,
                file_system=request_drive_sensor.file_system,
                all_space=request_drive_sensor.all_space,
                free_space=request_drive_sensor.free_space,
                frame_id=frame_id
            )
            drive_sensors.append(drive_sensor_model)
        session.add_all(drive_sensors)
