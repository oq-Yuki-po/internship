import datetime

import factory
from factory import Factory
from factory.faker import Faker

from app.schemas.requests import RecordSaveIn
from app.schemas.requests.factories import DriveSensorFactory, IpPortSensorFactory, ProcessSensorFactory, UserFactory


class RecordSaveInFactory(Factory):
    class Meta:

        model = RecordSaveIn

    @factory.lazy_attribute
    def created_at(self):
        date = datetime.datetime.now()
        return datetime.datetime.strftime(date, '%Y-%m-%d %H:%M:%S')

    user = UserFactory()
    session_id = Faker('uuid4')
    drive_sensors = [DriveSensorFactory()]
    ip_port_sensors = [IpPortSensorFactory()]
    process_sensors = [ProcessSensorFactory()]
    screenshot_sensor = {'image': 'sample image'}
