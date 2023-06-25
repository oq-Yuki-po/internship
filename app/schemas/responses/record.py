from pydantic import BaseModel, Field


class RecordSaveOut(BaseModel):

    message: str = Field(title='message', min_length=1, max_length=255)

    class Config:
        schema_extra = {
            'example': {
                'message': 'success'
            }
        }
