from pydantic import BaseModel, Field


class UserSession(BaseModel):
    """AllUserSession

    Attributes
    ----------
    id : int
        id
    sessionId : str
        sessionId
    startDate : str
        startDate (format: YYYY-MM-DD HH:mm:ss)
    endDate : str
        endDate (format: YYYY-MM-DD HH:mm:ss)
    userName : str
        userName
    machineName : str
        machineName
    """

    id: int = Field(title='id')
    sessionId: str = Field(title='sessionId', min_length=36, max_length=36)
    startDate: str = Field(title='startDate', min_length=19, max_length=19)
    endDate: str = Field(title='endDate', min_length=19, max_length=19)
    userName: str = Field(title='userName', min_length=1, max_length=40)
    machineName: str = Field(title='machineName', min_length=1, max_length=40)

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'sessionId': '8e140dd8-f921-4988-a91a-53cec6b3ad28',
                'startDate': '2021-01-01 00:00:00',
                'endDate': '2021-01-01 03:00:00',
                'userName': 'test',
                'machineName': 'test'
            }
        }


class GetUserSessionOut(BaseModel):

    user_sessions: list[UserSession] = Field(title='data')

    class Config:
        schema_extra = {
            'example': {
                'user_sessions': [UserSession.Config.schema_extra['example']]
            }
        }
