from datetime import datetime

from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory
from factory.faker import Faker

from app.models import UserModel, session


class UserFactory(SQLAlchemyModelFactory):
    """
    UserFactory

    Attributes
    ----------
    name : str
        user name
    ip : str
        user ip address
    machine_name : str
        user machine name
    created_at : datetime
        created datetime
    updated_at : datetime
        updated datetime
    """
    class Meta:

        model = UserModel
        sqlalchemy_session = session

    name = Sequence(lambda n: f'user_{n}')
    ip = Faker('ipv4')
    machine_name = Sequence(lambda n: f'machine_{n}')
    created_at = datetime.now()
    updated_at = datetime.now()
