from factory import Factory, Sequence
from factory.faker import Faker

from app.schemas.requests.sensors import ProcessSensor


class ProcessSensorFactory(Factory):
    class Meta:

        model = ProcessSensor

    file_path = Faker('file_path')
    process_name = Faker('file_name')
    process_id = Sequence(lambda n: n)
    started_at = "2021-01-01 00:00:00"
