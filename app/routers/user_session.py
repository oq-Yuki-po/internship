from fastapi import APIRouter

from app.models.frame import FrameModel
from app.routers.setting import AppRoutes
from app.schemas.responses import GetUserSessionOut, UserSession

router = APIRouter(
    prefix=AppRoutes.UserSessions.PREFIX,
    tags=[AppRoutes.UserSessions.TAG],
)


@router.get(AppRoutes.UserSessions.GET_URL,
            response_model=GetUserSessionOut,
            summary='Create a record')
async def get_user_sessions() -> GetUserSessionOut:
    """get user sessions

    Returns
    -------
    GetUserSessionOut
        user sessions
    """

    fetched_user_sessions = FrameModel.fetch_all_user_session()

    return GetUserSessionOut(user_sessions=[UserSession(id=user_session.id,
                                                        sessionId=user_session.session_id,
                                                        startDate=user_session.start_time,
                                                        endDate=user_session.end_time,
                                                        userName=user_session.name,
                                                        machineName=user_session.machine_name)
                                            for user_session in fetched_user_sessions])
