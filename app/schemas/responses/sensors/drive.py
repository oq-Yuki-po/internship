from pydantic import BaseModel, Field


class ResponseDriveSensor(BaseModel):  # pylint: disable=duplicate-code
    """Drive sensor schema for response body validation.

    Parameters
    ----------
    drive_letter : str
        Drive letter of the drive.
    drive_type : str
        Drive type of the drive.
    volume_name : str
        Volume name of the drive.
    file_system : str
        File system of the drive.
    all_space : str
        All space of the drive.
    free_space : str
        Free space of the drive.
    """

    drive_letter: str = Field(title='drive_letter', min_length=1, max_length=1)
    drive_type: str = Field(title='drive_type')
    volume_name: str = Field(title='volume_name', min_length=0, max_length=255)
    file_system: str = Field(title='file_system', min_length=0, max_length=255)
    all_space: str = Field(title='all_space', min_length=0, max_length=16)
    free_space: str = Field(title='free_space', min_length=0, max_length=16)

    class Config:
        schema_extra = {
            'example': {
                'drive_letter': 'C',
                'drive_type': 'Removable',
                'volume_name': 'Local Disk',
                'file_system': 'NTFS',
                'all_space': '512GB',
                'free_space': '112GB'
            }
        }
