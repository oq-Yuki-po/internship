from sqlalchemy import select

from app.models import DriveSensorModel
from app.models.factories import DriveSensorFactory, FrameFactory
from app.schemas.requests.sensors import RequestDriveSensor


class TestDriveSensor():

    def test_save_one_data(self, db_session):
        """
        Test save one data
        """

        frame = FrameFactory()
        db_session.add(frame)
        db_session.flush()

        excepted_drive_letter = "C"
        excepted_drive_type = 3
        excepted_volume_name = "Local Disk"
        excepted_file_system = "NTFS"
        excepted_all_space = "512GB"
        excepted_free_space = "256GB"

        request_drive_sensor = RequestDriveSensor(
            drive_letter=excepted_drive_letter,
            drive_type=excepted_drive_type,
            volume_name=excepted_volume_name,
            file_system=excepted_file_system,
            all_space=excepted_all_space,
            free_space=excepted_free_space
        )

        DriveSensorModel.save([request_drive_sensor], frame.id)

        db_session.commit()

        stmt = select(DriveSensorModel).where(DriveSensorModel.frame_id == frame.id)

        saved_drive_sensor = db_session.execute(stmt).scalar_one()

        assert saved_drive_sensor.frame_id == frame.id
        assert saved_drive_sensor.drive_letter == excepted_drive_letter
        assert saved_drive_sensor.drive_type == excepted_drive_type
        assert saved_drive_sensor.volume_name == excepted_volume_name
        assert saved_drive_sensor.file_system == excepted_file_system
        assert saved_drive_sensor.all_space == excepted_all_space
        assert saved_drive_sensor.free_space == excepted_free_space

    def test_save_multiple_data(self, db_session):
        """
        Test save multiple data
        """

        frame = FrameFactory()
        db_session.add(frame)
        db_session.flush()

        drive_sensors = DriveSensorFactory.build_batch(10)

        request_drive_sensors = []

        for drive_sensor in drive_sensors:
            request_drive_sensors.append(
                RequestDriveSensor(
                    drive_letter=drive_sensor.drive_letter,
                    drive_type=drive_sensor.drive_type,
                    volume_name=drive_sensor.volume_name,
                    file_system=drive_sensor.file_system,
                    all_space=drive_sensor.all_space,
                    free_space=drive_sensor.free_space
                )
            )

        DriveSensorModel.save(request_drive_sensors, frame.id)

        db_session.commit()

        stmt = select(DriveSensorModel.id).where(DriveSensorModel.frame_id == frame.id)

        saved_drive_sensors = db_session.execute(stmt).scalars().all()

        assert len(saved_drive_sensors) == 10
