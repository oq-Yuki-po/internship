from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.routers.setting import AppRoutes
from app.schemas.requests.factories import DriveSensorFactory, IpPortSensorFactory, ProcessSensorFactory, UserFactory
from app.schemas.responses import RecordSaveOut

TEST_URL = f"{AppRoutes.Records.PREFIX}"


def test_save(app_client: TestClient):

    drive_sensor = DriveSensorFactory()
    ip_port_sensor = IpPortSensorFactory()
    process_sensor = ProcessSensorFactory()
    user = UserFactory()

    request = {
        'user': user.dict(),
        'created_at': '2021-01-01 00:00:00',
        'drive_sensors': [drive_sensor.dict()],
        'ip_port_sensors': [ip_port_sensor.dict()],
        'process_sensors': [process_sensor.dict()],
        'screenshot_sensor': {'image': 'sample image'},
    }

    print(request)

    response = app_client.post(TEST_URL, json=request)

    assert response.status_code == 200
