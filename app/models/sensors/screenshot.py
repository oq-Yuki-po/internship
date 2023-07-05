from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.models import BaseModel, FrameModel, session
from app.schemas.requests.sensors import RequestScreenshotSensor


def decode_base64(base64_image: str) -> np.ndarray:
    """
    decode_base64

    Parameters
    ----------
    base64_image : str
        base64 image

    Returns
    -------
    image : np.ndarray
        image
    """

    image_stream = base64.b64decode(base64_image)

    image = cv2.imdecode(np.frombuffer(image_stream, dtype=np.uint8), cv2.IMREAD_COLOR)

    return image


def encode_base64(image: np.ndarray) -> str:
    """
    encode_base64

    Parameters
    ----------
    image : np.ndarray
        image

    Returns
    -------
    dst_str : str
        base64 image
    """

    dst_data = image.tobytes()

    dst_str = base64.b64encode(dst_data)

    return dst_str


class ScreenshotSensorModel(BaseModel):
    """
    ScreenshotSensorModel

    Attributes
    ----------
    id : int
        ip port
    image_path : str
        file path
    frame_id : int
        frame id
    frame : FrameModel
        frame
    """
    __tablename__ = 'screenshot_sensors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_path = Column(Text, nullable=False, comment='file path')
    frame_id = Column(Integer, ForeignKey(FrameModel.id), nullable=False, comment='frame id')
    frame = relationship(FrameModel, backref='screenshot_sensors')

    def __init__(self,
                 image_path: str,
                 frame_id: Optional[int] = None,
                 frame: Optional[FrameModel] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None) -> None:
        """
        Parameters
        ----------
        image_path : str
            image file path
        frame_id : Optional[int], optional
            frame id, by default None
        frame : Optional[FrameModel], optional
            frame, by default None
        created_at : Optional[datetime], optional
            created datetime, by default None
        updated_at : Optional[datetime], optional
            updated datetime, by default None
        """
        self.image_path = image_path
        if frame_id is not None:
            self.frame_id = frame_id
        elif frame is not None:
            self.frame = frame
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"<ScreenshotSensorModel(id={self.id}, image_path={self.image_path}, frame_id={self.frame_id}"\
            f", created_at={self.created_at}, updated_at={self.updated_at})>"

    @classmethod
    def save(cls,
             request_screenshot_sensor: RequestScreenshotSensor,
             frame_id: int,
             user_name: str,
             frame_create_time: datetime):
        """
        save

        Parameters
        ----------
        request_screenshot_sensor : ScreenshotSensorCreateRequest
            request screenshot sensor
        frame_id : int
            frame id
        user_name : str
            user name
        frame_create_time : datetime
            frame create time
        """

        image_path = cls._save_image(request_screenshot_sensor.image,
                                     frame_id,
                                     user_name,
                                     frame_create_time)

        screenshot_sensor = ScreenshotSensorModel(image_path=image_path, frame_id=frame_id)
        session.add(screenshot_sensor)

    @classmethod
    def _save_image(cls,
                    image: str,
                    frame_id: int,
                    user_name: str,
                    frame_create_time: str) -> str:
        """
        save image

        Parameters
        ----------
        image : str
            image
        frame_id : int
            frame id
        user_name : str
            user name
        frame_create_time : str
            frame create time

        Returns
        -------
        str
            saved image path
        """

        decoded_image = decode_base64(image)

        frame_create_time = frame_create_time.split(' ')
        date, time = frame_create_time[0], frame_create_time[1]
        year, month, day = date.split('-')
        hour, minute, second = time.split(':')

        save_path = f'./screenshots/{user_name}/{year}{month}{day}'
        Path(save_path).mkdir(parents=True, exist_ok=True)

        image_path = f'{save_path}/{hour}{minute}{second}_{frame_id}.png'

        cv2.imwrite(f'{image_path}', decoded_image)

        return image_path
