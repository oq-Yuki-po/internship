from sqlalchemy import select

from app.models import UserSessionModel
from app.models.factories import UserFactory, UserSessionFactory


class TestUserSessionModel:

    def test_fetch_by_session_id_data_exists(self, db_session):
        """
        test fetch user session by session id
        check fetched user session id is equal to saved user session id
        """

        user_session = UserSessionFactory()
        db_session.add(user_session)
        db_session.commit()
        session_id = user_session.session_id
        user_session_id = user_session.id
        db_session.close()

        fetched_user_session = UserSessionModel.fetch_by_session_id(session_id)

        assert fetched_user_session.id == user_session_id

    def test_fetch_by_session_id_data_not_exists(self):
        """
        test fetch user session by session id
        check fetched user session id is None
        """

        user_session = UserSessionFactory()

        fetched_user_session = UserSessionModel.fetch_by_session_id(user_session.session_id)

        assert fetched_user_session is None

    def test_save_data_not_exists(self, db_session):
        """
        test save user session
        check saved user session id, session_id, user_id is equal to fetched user session id, session_id, user_id
        """

        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        user_id = user.id
        db_session.close()

        test_session_id = '8e140dd8-f921-4988-a91a-53cec6b3ad28'

        user_session = UserSessionModel(session_id=test_session_id, user_id=user_id)
        user_session_id = UserSessionModel.save(user_session)

        db_session.commit()
        db_session.close()

        stmt = select(UserSessionModel).where(UserSessionModel.session_id == test_session_id)

        fetched_user_session = db_session.execute(stmt).scalar()

        assert user_session_id == fetched_user_session.id

    def test_save_data_exists(self, db_session):
        """
        test save user session
        check saved user session id, session_id, user_id is equal to fetched user session id, session_id, user_id
        """

        test_session_id = '8e140dd8-f921-4988-a91a-53cec6b3ad28'

        user = UserFactory()
        user_session = UserSessionFactory(user_id=user.id, session_id=test_session_id)
        db_session.add(user_session)
        db_session.commit()
        user_id = user.id
        user_session_id = user_session.id
        db_session.close()

        user_session = UserSessionModel(session_id=test_session_id, user_id=user_id)

        saved_user_session_id = UserSessionModel.save(user_session)

        db_session.commit()

        assert saved_user_session_id == user_session_id
