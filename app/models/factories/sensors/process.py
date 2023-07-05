from datetime import datetime

import factory
from factory import Faker, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import ProcessSensorModel, session
from app.models.factories import FrameFactory


class ProcessSensorFactory(SQLAlchemyModelFactory):
    """
    ProcessSensorFactory

    Attributes
    ----------
    file_path : str
        file path
    process_name : str
        process name
    process_id : int
        process id
    started_at : datetime
        started at
    frame : FrameModel
        frame
    created_at : datetime
        created at
    updated_at : datetime
        updated at
    """
    class Meta:

        model = ProcessSensorModel
        sqlalchemy_session = session

    @factory.lazy_attribute
    def started_at(self):
        date = datetime.now()
        return date.strftime('%Y-%m-%d %H:%M:%S')

    file_path = Faker('file_path')
    process_name = Faker('file_path')
    process_id = Faker('pyint')
    frame = SubFactory(FrameFactory)
    created_at = datetime.now()
    updated_at = datetime.now()
