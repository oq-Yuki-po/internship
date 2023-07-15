from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models import BaseModel, FrameModel, session
from app.models.setting import metadata
from app.schemas.requests.sensors.ip_port import IpPortType, RequestIpPortSensor


class IpPortSensorModel(BaseModel):
    """
    IpPortSensorModel

    Attributes
    ----------
    id : int
        ip port
    state : str
        ip port state. listen or establish
    ip : str
        ip address
    port : int
        port
    process_id : int
        process id
    remote_ip : str
        remote ip address
    remote_port : int
        remote port
    frame_id : int
        frame id
    frame : FrameModel
        frame
    """
    __tablename__ = 'ip_port_sensors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(String(10), comment='ip port state. listen or establish')
    ip = Column(String(39), nullable=False, comment='ip address')
    port = Column(Integer, nullable=False, comment='port')
    process_id = Column(Integer, nullable=False, comment='process id')
    remote_ip = Column(String(39), nullable=False, comment='remote ip address')
    remote_port = Column(Integer, nullable=False, comment='remote port')
    frame_id = Column(Integer, ForeignKey(FrameModel.id), nullable=False, comment='frame id')

    frame = relationship(FrameModel, backref='ip_port_sensors')
    UniqueConstraint("state",
                     "ip",
                     "port",
                     "process_id",
                     "remote_ip",
                     "remote_port",
                     "frame_id",
                     name="unique_ip_port")

    def __init__(self,
                 state: str,
                 ip: str,
                 port: int,
                 process_id: int,
                 remote_ip: str,
                 remote_port: int,
                 frame_id: Optional[int] = None,
                 frame: Optional[FrameModel] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:
        """
        Parameters
        ----------
        state : str
            ip port state. listen or establish
        ip : str
            ip address
        port : int
            port
        process_id : int
            process id
        remote_ip : str
            remote ip address
        remote_port : int
            remote port
        frame_id : Optional[int], optional
            frame id, by default None
        frame : Optional[FrameModel], optional
            frame, by default None
        created_at : Optional[datetime], optional
            created datetime, by default None
        updated_at : Optional[datetime], optional
            updated datetime, by default None
        """
        self.state = state
        self.ip = ip
        self.port = port
        self.process_id = process_id
        self.remote_ip = remote_ip
        self.remote_port = remote_port

        if frame_id is not None:
            self.frame_id = frame_id
        elif frame is not None:
            self.frame = frame
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"< IpPortSensor id={self.id} state={self.state} ip={self.ip} port={self.port} " \
            f"process_id={self.process_id} remote_ip={self.remote_ip} remote_port={self.remote_port} " \
            f"frame_id={self.frame_id} created_at={self.created_at} updated_at={self.updated_at} >"

    @classmethod
    def save(cls, request_ip_port_sensors: list[RequestIpPortSensor], frame_id: int) -> None:
        """Save ip port sensors.

        Parameters
        ----------
        request_ip_port_sensors : list[RequestIpPortSensor]
            ip port sensors
        frame_id : int
            frame id
        """
        ip_port_sensors = []

        for request_ip_port_sensor in request_ip_port_sensors:
            ip_port_sensor_model = cls(
                state=request_ip_port_sensor.state.value,
                ip=request_ip_port_sensor.ip,
                port=request_ip_port_sensor.port,
                process_id=request_ip_port_sensor.process_id,
                remote_ip=request_ip_port_sensor.remote_ip,
                remote_port=request_ip_port_sensor.remote_port,
                frame_id=frame_id
            )
            ip_port_sensors.append(ip_port_sensor_model)

        session.add_all(ip_port_sensors)
