from pydantic import BaseModel, Field


class ResponseProcessSensor(BaseModel):
    """
    Process sensor schema for response body validation.

    Parameters
    ----------
    file_path : str
        File path of the process.
    process_name : str
        Process name of the process.
    process_id : int
        Process id of the process.
    started_at : str
        Started at of the process.
    """

    file_path: str = Field(title='file_path', min_length=1, max_length=255)
    process_name: str = Field(title='process_name', min_length=1, max_length=255)
    process_id: int = Field(title='process_id', ge=0, le=65535)
    started_at: str = Field(title='started_at', min_length=19, max_length=19)

    class Config:
        schema_extra = {
            'example': {
                'file_path': 'C:\\Windows\\System32\\svchost.exe',
                'process_name': 'svchost.exe',
                'process_id': 1234,
                'started_at': '2021-01-01 00:00:00'
            }
        }
