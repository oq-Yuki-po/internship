from datetime import datetime

import factory
from factory import SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import FrameModel, session
from app.models.factories import UserSessionFactory


class FrameFactory(SQLAlchemyModelFactory):
    """
    FrameFactory

    Attributes
    ----------

    """
    class Meta:

        model = FrameModel
        sqlalchemy_session = session

    @factory.lazy_attribute
    def frame_create_time(self):
        date = datetime.now()
        return date.time()

    # frame_create_time = Faker('date_time_between', start_date='-1y', end_date='now')
    user_session = SubFactory(UserSessionFactory)
    created_at = datetime.now()
    updated_at = datetime.now()
