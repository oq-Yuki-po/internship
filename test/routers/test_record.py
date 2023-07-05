# import json

# from fastapi.encoders import jsonable_encoder
# from fastapi.testclient import TestClient

# from app.routers.setting import AppRoutes
# from app.schemas.requests.factories import DriveSensorFactory, IpPortSensorFactory, ProcessSensorFactory, UserFactory
# from app.schemas.responses import RecordSaveOut

# TEST_URL = f"{AppRoutes.Records.PREFIX}"


# def test_save(app_client: TestClient):

#     drive_sensor = DriveSensorFactory()
#     ip_port_sensor = IpPortSensorFactory()
#     process_sensor = ProcessSensorFactory()
#     user = UserFactory()

#     request = {
#         'user': user.dict(),
#         'session_id': '8e140dd8-f921-4988-a91a-53cec6b3ad28',
#         'created_at': '2021-01-01 00:00:00',
#         'drive_sensors': [drive_sensor.dict()],
#         'ip_port_sensors': [ip_port_sensor.dict()],
#         'process_sensors': [process_sensor.dict()],
#         'screenshot_sensor': {'image': 'sample image'},
#     }

#     jsonable_encoder(json.dumps(request))

#     response = app_client.post(TEST_URL, json=json.dumps(request))

#     assert response.status_code == 200
