from datetime import datetime

from factory import SubFactory, Faker
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice

from app.models import IpPortSensorModel, session
from app.models.factories import FrameFactory
from app.schemas.requests.sensors import IpPortType


class IpPortSensorFactory(SQLAlchemyModelFactory):
    """
    IpPortSensor

    Attributes
    ----------
    state : IpPortType
        ip port type enum. listen or establish
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
    frame : FrameModel
        frame
    created_at : datetime
        created at
    updated_at : datetime
        updated at
    """
    class Meta:

        model = IpPortSensorModel
        sqlalchemy_session = session

    state = FuzzyChoice([e.value for e in list(IpPortType)])
    ip = Faker('ipv4')
    port = Faker('port_number')
    process_id = Faker('pyint')
    remote_ip = Faker('ipv4')
    remote_port = Faker('port_number')
    frame = SubFactory(FrameFactory)
    created_at = datetime.now()
    updated_at = datetime.now()
