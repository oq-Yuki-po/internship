from enum import Enum

from pydantic import BaseModel, Field


class IpPortType(str, Enum):
    """IpPort type enum."""
    listen = 0
    establish = 1


class IpPortSensor(BaseModel):
    """IpPort sensor schema for request body validation.

    Parameters
    ----------
    state : IpPortType
        State of the sensor.
    ip : str
        Ip of the sensor.
    port : int
        Port of the sensor.
    process_id : int
        Process id of the sensor.
    remote_ip : str
        Remote ip of the sensor.
    remote_port : int
        Remote port of the sensor.
    """

    state: IpPortType = Field(title='state')
    ip: str = Field(title='ip', min_length=1, max_length=39)
    port: int = Field(title='port', ge=1, le=65535)
    process_id: int = Field(title='process_id', ge=0, le=65535)

    remote_ip: str = Field(title='remote_ip', min_length=1, max_length=39)
    remote_port: int = Field(title='remote_port', ge=1, le=65535)

    class Config:
        schema_extra = {
            'example': {
                'state': 0,
                'ip': '192.168.12.5',
                'port': 80,
                'process_id': 0,
                'remote_ip': '172.16.31.50',
                'remote_port': 0
            }
        }
