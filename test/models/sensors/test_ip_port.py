from sqlalchemy import select

from app.models import IpPortSensorModel
from app.models.factories import FrameFactory, IpPortSensorFactory
from app.schemas.requests.sensors import IpPortType, RequestIpPortSensor


class TestIpPortSensor():

    def test_save_one_data(self, db_session):
        """
        Test save one data
        """

        frame = FrameFactory()
        db_session.add(frame)
        db_session.flush()

        excepted_state = IpPortType.listen
        excepted_ip = '192.102.222.234'
        excepted_port = 8080
        excepted_process_id = 1234
        excepted_remote_ip = '123.11.23.111'
        excepted_remote_port = 8080

        request_ip_port_sensor = RequestIpPortSensor(
            state=excepted_state.value,
            ip=excepted_ip,
            port=excepted_port,
            process_id=excepted_process_id,
            remote_ip=excepted_remote_ip,
            remote_port=excepted_remote_port
        )

        IpPortSensorModel.save([request_ip_port_sensor], frame.id)

        db_session.commit()

        stmt = select(IpPortSensorModel).where(IpPortSensorModel.frame_id == frame.id)

        saved_ip_port_sensor = db_session.execute(stmt).scalar_one()

        assert saved_ip_port_sensor.state == excepted_state.name
        assert saved_ip_port_sensor.ip == excepted_ip
        assert saved_ip_port_sensor.port == excepted_port
        assert saved_ip_port_sensor.process_id == excepted_process_id
        assert saved_ip_port_sensor.remote_ip == excepted_remote_ip
        assert saved_ip_port_sensor.remote_port == excepted_remote_port

    def test_save_multiple_data(self, db_session):
        """
        Test save multiple data
        """

        frame = FrameFactory()
        db_session.add(frame)
        db_session.flush()

        ip_port_sensors = IpPortSensorFactory.build_batch(10)

        request_ip_port_sensors = []

        for drive_sensor in ip_port_sensors:
            request_ip_port_sensors.append(
                RequestIpPortSensor(
                    state=drive_sensor.state,
                    ip=drive_sensor.ip,
                    port=drive_sensor.port,
                    process_id=drive_sensor.process_id,
                    remote_ip=drive_sensor.remote_ip,
                    remote_port=drive_sensor.remote_port
                )
            )

        IpPortSensorModel.save(request_ip_port_sensors, frame.id)

        db_session.commit()

        stmt = select(IpPortSensorModel.id).where(IpPortSensorModel.frame_id == frame.id)

        saved_drive_sensors = db_session.execute(stmt).scalars().all()

        assert len(saved_drive_sensors) == 10
