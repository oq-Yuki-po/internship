from pydantic import BaseModel, Field

from app.schemas.responses.sensors import (
    ResponseDriveSensor,
    ResponseIpPortSensor,
    ResponseProcessSensor,
    ResponseScreenshotSensor,
)


class GetFrameOut(BaseModel):

    record_time: str = Field(title='record_time', min_length=19, max_length=19)
    drive_sensors: list[ResponseDriveSensor] = Field(title='drive_sensor',
                                                     description='drive_sensor')
    ip_port_sensors: list[ResponseIpPortSensor] = Field(title='ip_port_sensor',
                                                        description='ip_port_sensor')
    process_sensors: list[ResponseProcessSensor] = Field(title='process_sensor',
                                                         description='process_sensor')
    screenshot_sensor: ResponseScreenshotSensor = Field(title='screenshot_sensor',
                                                        description='screenshot_sensor')

    class Config:
        schema_extra = {
            'example': {
                'record_time': '2021-01-01 00:00:00',
                'drive_sensors': [ResponseDriveSensor.Config.schema_extra['example']],
                'ip_port_sensors': [ResponseIpPortSensor.Config.schema_extra['example']],
                'process_sensors': [ResponseProcessSensor.Config.schema_extra['example']],
                'screenshot_sensor': ResponseScreenshotSensor.Config.schema_extra['example']
            }
        }
