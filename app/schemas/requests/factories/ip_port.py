from factory import Factory, Sequence
from factory.faker import Faker

from app.schemas.requests.sensors import IpPortSensor


class IpPortSensorFactory(Factory):
    class Meta:

        model = IpPortSensor

    state = "0"
    ip = Faker('ipv4')
    port = Faker('port_number')
    process_id = Sequence(lambda n: n)
    remote_ip = Faker('ipv4')
    remote_port = Faker('port_number')
