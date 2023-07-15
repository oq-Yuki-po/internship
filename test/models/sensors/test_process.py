from datetime import datetime

from sqlalchemy import select

from app.models import ProcessSensorModel
from app.models.factories import FrameFactory, ProcessSensorFactory
from app.schemas.requests.sensors import RequestProcessSensor


class TestProcessSensor():

    def test_save_one_data(self, db_session):
        """
        Test save one data
        """

        frame = FrameFactory()
        db_session.add(frame)
        db_session.flush()

        excepted_file_path = '/usr/bin/python'
        excepted_process_name = 'python'
        excepted_process_id = 1234
        excepted_started_at = '2021-01-01 00:00:00'

        request_process_sensor = RequestProcessSensor(
            file_path=excepted_file_path,
            process_name=excepted_process_name,
            process_id=excepted_process_id,
            started_at=excepted_started_at
        )

        ProcessSensorModel.save([request_process_sensor], frame.id)

        db_session.commit()

        stmt = select(ProcessSensorModel).where(ProcessSensorModel.frame_id == frame.id)

        saved_process_sensor = db_session.execute(stmt).scalar_one()

        assert saved_process_sensor.file_path == excepted_file_path
        assert saved_process_sensor.process_name == excepted_process_name
        assert saved_process_sensor.process_id == excepted_process_id
        assert saved_process_sensor.started_at == datetime.strptime(excepted_started_at, '%Y-%m-%d %H:%M:%S')

    def test_save_multiple_data(self, db_session):
        """
        Test save multiple data
        """

        frame = FrameFactory()
        db_session.add(frame)
        db_session.flush()

        process_sensors = ProcessSensorFactory.build_batch(10)

        request_process_sensors = []

        for process_sensor in process_sensors:
            request_process_sensor = RequestProcessSensor(
                file_path=process_sensor.file_path,
                process_name=process_sensor.process_name,
                process_id=process_sensor.process_id,
                started_at=process_sensor.started_at
            )
            request_process_sensors.append(request_process_sensor)

        ProcessSensorModel.save(request_process_sensors, frame.id)

        db_session.commit()

        stmt = select(ProcessSensorModel).where(ProcessSensorModel.frame_id == frame.id)

        saved_process_sensors = db_session.execute(stmt).scalars().all()

        assert len(saved_process_sensors) == 10

    def test_fetch_by_frame_id(self, db_session):

        frame = FrameFactory()
        process_sensor_1 = ProcessSensorFactory(frame=frame)
        process_sensor_2 = ProcessSensorFactory(frame=frame)
        db_session.add_all([frame, process_sensor_1, process_sensor_2])
        db_session.flush()
        frame_id = frame.id
        db_session.commit()

        process_sensors = ProcessSensorModel.fetch_by_frame_id(frame_id)

        assert len(process_sensors) == 2
