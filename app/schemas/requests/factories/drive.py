from factory import Factory
from factory.fuzzy import FuzzyChoice

from app.schemas.requests.sensors import DriveType, RequestDriveSensor


class DriveSensorFactory(Factory):
    class Meta:

        model = RequestDriveSensor

    drive_letter = "C"
    drive_type = FuzzyChoice([e.value for e in list(DriveType)])
    volume_name = 'Local Disk'
    file_system = 'NTFS'
    all_space = '512GB'
    free_space = '112GB'
