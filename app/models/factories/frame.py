from datetime import datetime

from factory.alchemy import SQLAlchemyModelFactory
from factory.faker import Faker

from app.models import FrameModel, session
from app.models.factories import UserFactory


class FrameFactory(SQLAlchemyModelFactory):
    """
    FrameFactory

    Attributes
    ----------

    """
    class Meta:

        model = FrameModel
        sqlalchemy_session = session

    frame_create_time = Faker('date_time_between', start_date='-1y', end_date='now')
    user = UserFactory()
    created_at = datetime.now()
    updated_at = datetime.now()
