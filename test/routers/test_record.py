import base64
import os

import cv2
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.routers.setting import AppRoutes
from app.schemas.requests.factories import RecordSaveInFactory, UserFactory
from app.schemas.responses import RecordSaveOut

TEST_URL = f"{AppRoutes.Records.PREFIX}"


def test_save(app_client: TestClient):

    test_user_name = 'test_user'
    test_created_at = '2012-01-01 00:00:00'
    test_date, test_time = test_created_at.split(' ')
    test_date = test_date.replace('-', '')
    test_time = test_time.replace(':', '')

    sample_image = cv2.imread('test/images/sample.png')

    _, dst_data = cv2.imencode('.png', sample_image)

    dst_str = base64.b64encode(dst_data)

    request = RecordSaveInFactory(
        user=UserFactory(name=test_user_name),
        created_at=test_created_at,
        screenshot_sensor={'image': dst_str},
    )

    response = app_client.post(TEST_URL, json=jsonable_encoder(request))

    assert response.status_code == 200
    assert response.json() == jsonable_encoder(RecordSaveOut(message='success'))
    assert os.path.exists(f"./screenshots/{test_user_name}/{test_date}/{test_time}_1.png")

    os.remove(f"./screenshots/{test_user_name}/{test_date}/{test_time}_1.png")
    os.rmdir(f"./screenshots/{test_user_name}/{test_date}")
    os.rmdir(f"./screenshots/{test_user_name}")
