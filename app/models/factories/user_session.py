from datetime import datetime

from factory import SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from factory.faker import Faker

from app.models import UserSessionModel, session
from app.models.factories import UserFactory


class UserSessionFactory(SQLAlchemyModelFactory):
    """
    UserSessionFactory

    Attributes
    ----------
    session_id : str
        session id which is uuid.
        represents the session between when the user opens and closes the PC.
    user : UserModel
        user
    created_at : datetime
        created datetime
    updated_at : datetime
        updated datetime
    """
    class Meta:

        model = UserSessionModel
        sqlalchemy_session = session

    session_id = Faker('uuid4')
    user = SubFactory(UserFactory)
    created_at = datetime.now()
    updated_at = datetime.now()
