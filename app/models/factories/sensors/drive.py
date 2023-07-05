from datetime import datetime

from factory import SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyChoice

from app.models import DriveSensorModel, session
from app.models.factories import FrameFactory
from app.schemas.requests.sensors import DriveType


class DriveSensorFactory(SQLAlchemyModelFactory):
    """
    DriveSensorFactory

    Attributes
    ----------
    drive_type : str
        drive type
    volume_name : str
        volume name
    file_system : str
        file system
    all_space : str
        all space
    free_space : str
        free space
    frame : FrameModel
        frame
    created_at : datetime
        created at
    updated_at : datetime
        updated at
    """
    class Meta:

        model = DriveSensorModel
        sqlalchemy_session = session

    drive_letter = "C"
    drive_type = FuzzyChoice([e.value for e in list(DriveType)])
    volume_name = "Local Disk"
    file_system = "NTFS"
    all_space = "512GB"
    free_space = "256GB"
    frame = SubFactory(FrameFactory)
    created_at = datetime.now()
    updated_at = datetime.now()
