from pydantic import BaseModel, Field

from app.schemas.requests.sensors import (
    RequestDriveSensor,
    RequestIpPortSensor,
    RequestProcessSensor,
    RequestScreenshotSensor,
)
from app.schemas.requests.user import User


class RecordSaveIn(BaseModel):
    """
    Record schema for request body validation.

    Parameters
    ----------
    user : User
        User schema.
    created_at : str
        Created at of the record.
    session_id : str
        session id of the record
    drive_sensor : list[RequestDriveSensor]
        Drive sensor schema list.
    ip_port_sensor : list[RequestIpPortSensor]
        Ip port sensor schema list.
    process_sensor : list[RequestProcessSensorsSensorsSensorsSensorsSensorsSensor]
        Process sensor schema list.
    screenshot_sensor : RequestScreenshotSensor
        Screenshot sensor schema.
    """

    user: User = Field(title='user', description='user')
    created_at: str = Field(title='created_at', min_length=19, max_length=19)
    session_id: str = Field(title='session id', min_length=36, max_length=36)
    drive_sensors: list[RequestDriveSensor] = Field(title='drive_sensor',
                                                    description='drive_sensor')
    ip_port_sensors: list[RequestIpPortSensor] = Field(title='ip_port_sensor',
                                                       description='ip_port_sensor')
    process_sensors: list[RequestProcessSensor] = Field(title='process_sensor',
                                                        description='process_sensor')
    screenshot_sensor: RequestScreenshotSensor = Field(title='screenshot_sensor',
                                                       description='screenshot_sensor')

    class Config:
        schema_extra = {
            'example': {
                'user': User.Config.schema_extra['example'],
                'created_at': '2021-01-01 00:00:00',
                'session_id': '8e140dd8-f921-4988-a91a-53cec6b3ad28',
                'drive_sensors': [RequestDriveSensor.Config.schema_extra['example']],
                'ip_port_sensors': [RequestIpPortSensor.Config.schema_extra['example']],
                'process_sensors': [RequestProcessSensor.Config.schema_extra['example']],
                'screenshot_sensor': RequestScreenshotSensor.Config.schema_extra['example']
            }
        }
