from pydantic import BaseModel, Field


class RequestScreenshotSensor(BaseModel):
    """
    Screenshot sensor schema for request body validation.

    Parameters
    ----------
    image : str
        Base64 encoded image.
    """

    image: str = Field(title='image', min_length=1, description='base64 encoded image')

    class Config:
        schema_extra = {
            'example': {
                'image': 'base64 encoded image'
            }
        }
