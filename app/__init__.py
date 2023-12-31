from functools import wraps

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.errors.custom_exception import CustomException
from app.errors.message import ErrorMessage
from app.logger import app_logger
from app.models import session


def handle_errors(func):
    """
    handle_errors is a decorator that handles errors.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except CustomException as exc:
            raise CustomException(detail=exc.detail, status_code=exc.status_code) from exc
        except HTTPException as exc:
            app_logger.error(exc)
            raise HTTPException(detail=ErrorMessage.INTERNAL_SERVER_ERROR, status_code=500) from exc
        except SQLAlchemyError as exc:
            app_logger.error(exc)
            raise HTTPException(detail=ErrorMessage.INTERNAL_SERVER_ERROR, status_code=500) from exc
        except Exception as exc:
            app_logger.error(exc)
            raise HTTPException(detail=ErrorMessage.INTERNAL_SERVER_ERROR, status_code=500) from exc
        finally:
            session.close()
    return wrapper
