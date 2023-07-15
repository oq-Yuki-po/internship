import base64
import os

import cv2
from sqlalchemy import select

from app.models import ScreenshotSensorModel
from app.models.factories import FrameFactory
from app.schemas.requests.sensors import RequestScreenshotSensor


class TestScreenshotSensor():

    def test__save_image(self):
        """
        Test save image
        """

        sample_image = cv2.imread('test/images/sample.png')

        _, dst_data = cv2.imencode('.png', sample_image)

        dst_str = base64.b64encode(dst_data)

        image_path = ScreenshotSensorModel._save_image(dst_str, 1, "sample_user", "2012-01-01 00:00:00")

        assert image_path == "./screenshots/sample_user/20120101/000000_1.png"
        assert os.path.exists('./screenshots/sample_user/20120101/000000_1.png')

        os.remove('./screenshots/sample_user/20120101/000000_1.png')
        os.rmdir('./screenshots/sample_user/20120101')
        os.rmdir('./screenshots/sample_user')

    def test_save(self, db_session):
        """
        Test save
        """

        frame = FrameFactory()
        db_session.add(frame)
        db_session.flush()
        frame_id = frame.id

        sample_image = cv2.imread('test/images/sample.png')

        _, dst_data = cv2.imencode('.png', sample_image)

        dst_str = base64.b64encode(dst_data)

        request_screenshot_sensor = RequestScreenshotSensor(image=dst_str)

        ScreenshotSensorModel.save(request_screenshot_sensor,
                                   frame_id,
                                   "sample_user",
                                   "2012-01-01 00:00:00")

        db_session.commit()

        stmt = select(ScreenshotSensorModel).where(ScreenshotSensorModel.frame_id == frame_id)

        saved_screenshot_sensor = db_session.execute(stmt).scalar_one()

        assert saved_screenshot_sensor.frame_id == frame_id
        assert saved_screenshot_sensor.image_path == "./screenshots/sample_user/20120101/000000_1.png"
        assert os.path.exists('./screenshots/sample_user/20120101/000000_1.png')

        os.remove('./screenshots/sample_user/20120101/000000_1.png')
        os.rmdir('./screenshots/sample_user/20120101')
        os.rmdir('./screenshots/sample_user')

    def test_fetch_by_frame_id(self, db_session):

        frame = FrameFactory()
        db_session.add(frame)
        db_session.flush()
        frame_id = frame.id
        screen_shot_sensor = ScreenshotSensorModel(image_path="test/images/sample.png", frame_id=frame_id)
        db_session.add(screen_shot_sensor)
        db_session.commit()

        encoded_screenshot_image = ScreenshotSensorModel.fetch_by_frame_id(frame_id)

        assert type(encoded_screenshot_image) == bytes
