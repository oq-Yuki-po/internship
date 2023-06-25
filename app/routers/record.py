from fastapi import APIRouter
from app.models import session
from app.routers.setting import AppRoutes
from app.schemas.responses import RecordSaveOut
from app.schemas.requests import RecordSaveIn

router = APIRouter(
    prefix=AppRoutes.Records.PREFIX,
    tags=[AppRoutes.Records.TAG],
)


@router.post(AppRoutes.Records.POST_URL,
             response_model=RecordSaveOut,
             summary='Create a record')
async def save(record: RecordSaveIn) -> RecordSaveOut:
    try:
        print(record)

        return RecordSaveOut(message='success')
    finally:
        session.close()
