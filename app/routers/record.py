from fastapi import APIRouter

from app.models import session
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
async def save(record: RecordSaveIn) -> RecordSaveOut:
    try:

        return RecordSaveOut(message='success')
    finally:
        session.close()
