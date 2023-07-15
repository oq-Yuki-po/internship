from fastapi import APIRouter

from app import handle_errors
from app.models import DriveSensorModel, FrameModel, IpPortSensorModel, ProcessSensorModel, ScreenshotSensorModel
from app.routers.setting import AppRoutes
from app.schemas.responses import GetFrameOut
from app.schemas.responses.sensors import (
    ResponseDriveSensor,
    ResponseIpPortSensor,
    ResponseProcessSensor,
    ResponseScreenshotSensor,
)

router = APIRouter(
    prefix=AppRoutes.Frames.PREFIX,
    tags=[AppRoutes.Frames.TAG],
)


@router.get(AppRoutes.Frames.GET_URL,
            response_model=GetFrameOut,
            summary='Get a frame')
@handle_errors
async def get_frame(session_id: str, frame_no: str) -> GetFrameOut:

    frame_model = FrameModel.fetch_frame_by_session_id_frame_no(session_id=session_id, frame_no=int(frame_no))

    frame_id, frame_create_time = frame_model.id, frame_model.frame_create_time

    drive_sensor_models = DriveSensorModel.fetch_by_frame_id(frame_id=frame_id)
    ip_port_sensor_models = IpPortSensorModel.fetch_by_frame_id(frame_id=frame_id)
    process_sensor_models = ProcessSensorModel.fetch_by_frame_id(frame_id=frame_id)
    screenshot_image = ScreenshotSensorModel.fetch_by_frame_id(frame_id=frame_id)

    drive_sensors = [
        ResponseDriveSensor(
            drive_letter=drive_sensor_model.drive_letter,
            drive_type=drive_sensor_model.drive_type,
            volume_name=drive_sensor_model.volume_name,
            file_system=drive_sensor_model.file_system,
            all_space=drive_sensor_model.all_space,
            free_space=drive_sensor_model.free_space)
        for drive_sensor_model in drive_sensor_models]

    ip_port_sensors = [
        ResponseIpPortSensor(
            state=ip_port_sensor_model.state,
            ip=ip_port_sensor_model.ip,
            port=ip_port_sensor_model.port,
            process_id=ip_port_sensor_model.process_id,
            remote_ip=ip_port_sensor_model.remote_ip,
            remote_port=ip_port_sensor_model.remote_port)
        for ip_port_sensor_model in ip_port_sensor_models]

    process_sensors = [
        ResponseProcessSensor(
            file_path=process_sensor_model.file_path,
            process_name=process_sensor_model.process_name,
            process_id=process_sensor_model.process_id,
            started_at=process_sensor_model.started_at)
        for process_sensor_model in process_sensor_models]

    screenshot_sensor = ResponseScreenshotSensor(image=screenshot_image)

    return GetFrameOut(record_time=frame_create_time,
                       drive_sensors=drive_sensors,
                       ip_port_sensors=ip_port_sensors,
                       process_sensors=process_sensors,
                       screenshot_sensor=screenshot_sensor)
