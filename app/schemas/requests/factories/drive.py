from factory import Factory

from app.schemas.requests.sensors import DriveSensor


class DriveSensorFactory(Factory):
    class Meta:

        model = DriveSensor

    drive_letter = "C"
    drive_type = 3
    volume_name = 'Local Disk'
    file_system = 'NTFS'
    all_space = '512GB'
    free_space = '112GB'
