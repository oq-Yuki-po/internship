from fastapi import APIRouter

from app import handle_errors
from app.models import (
    DriveSensorModel,
    FrameModel,
    IpPortSensorModel,
    ProcessSensorModel,
    ScreenshotSensorModel,
    UserModel,
    UserSessionModel,
    session,
)
from app.routers.setting import AppRoutes
from app.schemas.requests import RecordSaveIn
from app.schemas.responses import RecordSaveOut

router = APIRouter(
    prefix=AppRoutes.Records.PREFIX,
    tags=[AppRoutes.Records.TAG],
)


@router.post(AppRoutes.Records.POST_URL,
             response_model=RecordSaveOut,
             summary='Create a record')
@handle_errors
async def save(record: RecordSaveIn) -> RecordSaveOut:
    # ユーザの登録
    user = record.user

    user_model = UserModel(name=user.name,
                           machine_name=user.machine_name,
                           ip=user.ip)

    use_id = UserModel.save(user_model)

    # セッションの登録
    session_id = record.session_id
    created_at = record.created_at
    user_session_model = UserSessionModel(session_id=session_id,
                                          user_id=use_id)
    user_session_id = UserSessionModel.save(user_session_model)

    # フレームの登録
    frame_model = FrameModel(frame_create_time=created_at,
                             user_session_id=user_session_id)
    frame_id = FrameModel.save(frame_model)

    # 各センサーの登録
    # drive
    drive_sensors = record.drive_sensors
    DriveSensorModel.save(drive_sensors, frame_id)

    # ip_port
    ip_port_sensors = record.ip_port_sensors
    IpPortSensorModel.save(ip_port_sensors, frame_id)

    # process
    process_sensors = record.process_sensors
    ProcessSensorModel.save(process_sensors, frame_id)

    # screenshot
    screenshot = record.screenshot_sensor
    ScreenshotSensorModel.save(screenshot, frame_id, user.name, created_at)

    session.commit()

    return RecordSaveOut(message='success')
