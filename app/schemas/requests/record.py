from pydantic import BaseModel, Field

from app.schemas.requests.sensors import DriveSensor, IpPortSensor, ProcessSensor, ScreenshotSensor
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
    drive_sensor : list[DriveSensor]
        Drive sensor schema list.
    ip_port_sensor : list[IpPortSensor]
        Ip port sensor schema list.
    process_sensor : list[ProcessSensor]
        Process sensor schema list.
    screenshot_sensor : ScreenshotSensor
        Screenshot sensor schema.
    """

    user: User = Field(title='user', description='user')
    created_at: str = Field(title='created_at', min_length=19, max_length=19)
    session_id: str = Field(title='session id', min_length=32, max_length=32)
    drive_sensors: list[DriveSensor] = Field(title='drive_sensor',
                                             description='drive_sensor')
    ip_port_sensors: list[IpPortSensor] = Field(title='ip_port_sensor',
                                                description='ip_port_sensor')
    process_sensors: list[ProcessSensor] = Field(title='process_sensor',
                                                 description='process_sensor')
    screenshot_sensor: ScreenshotSensor = Field(title='screenshot_sensor',
                                                description='screenshot_sensor')

    class Config:
        schema_extra = {
            'example': {
                'user': User.Config.schema_extra['example'],
                'created_at': '2021-01-01 00:00:00',
                'session_id': 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
                'drive_sensors': [DriveSensor.Config.schema_extra['example']],
                'ip_port_sensors': [IpPortSensor.Config.schema_extra['example']],
                'process_sensors': [ProcessSensor.Config.schema_extra['example']],
                'screenshot_sensor': ScreenshotSensor.Config.schema_extra['example']
            }
        }
