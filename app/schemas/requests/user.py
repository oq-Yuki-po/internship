from pydantic import BaseModel, Field


class User(BaseModel):
    """User schema for request body validation.

    Parameters
    ----------
    machine_name : str
        Machine name of the user.
    name : str
        Name of the user.
    ip_address : str
        IP address of the user.
    """
    machine_name: str = Field(title='machine_name', min_length=1, max_length=255)
    name: str = Field(title='user_name', min_length=1, max_length=255)
    ip_address: str = Field(title='ip_address', min_length=1, max_length=39)

    class Config:
        schema_extra = {
            'example': {
                'machine_name': 'sample machine name',
                'name': 'sample user name',
                'ip_address': '192.168.4.13'
            }
        }
