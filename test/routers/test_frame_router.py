from fastapi.testclient import TestClient

from app.models import ScreenshotSensorModel
from app.models.factories import (
    DriveSensorFactory,
    FrameFactory,
    IpPortSensorFactory,
    ProcessSensorFactory,
    UserSessionFactory,
)
from app.routers.setting import AppRoutes

TEST_URL = f"{AppRoutes.Frames.PREFIX}"


def test_get_frame(app_client: TestClient, db_session):

    user_session_model = UserSessionFactory()
    frame_model = FrameFactory(user_session=user_session_model)
    drive_sensor_models = DriveSensorFactory.build_batch(2, frame=frame_model)
    ip_port_sensor_models = IpPortSensorFactory.build_batch(3, frame=frame_model)
    process_sensor_models = ProcessSensorFactory.build_batch(5, frame=frame_model)
    screenshot_sensor_model = ScreenshotSensorModel(frame=frame_model, image_path='test/images/sample.png')

    db_session.add_all([
        user_session_model,
        frame_model,
        screenshot_sensor_model])
    db_session.add_all(drive_sensor_models)
    db_session.add_all(ip_port_sensor_models)
    db_session.add_all(process_sensor_models)
    db_session.flush()
    user_session_id = user_session_model.session_id
    frame_no = 1
    db_session.commit()

    response = app_client.get(f"{TEST_URL}/{user_session_id}/{frame_no}")

    assert response.status_code == 200
    response_json = response.json()

    assert len(response_json['drive_sensors']) == 2
    assert len(response_json['ip_port_sensors']) == 3
    assert len(response_json['process_sensors']) == 5
