from sqlalchemy import select

from app.models.factories import UserFactory
from app.models.user import UserModel


class TestUser():

    def test_fetch_name_ip_machine_name_data_exists(self, db_session):
        """
        test fetch user by name, ip, machine_name
        check fetched user id is equal to saved user id
        """

        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        user_id, user_name, user_ip, user_machine_name = user.id, user.name, user.ip, user.machine_name
        db_session.close()

        fetched_user = UserModel.fetch_by_name_ip_machine_name(user_name, user_ip, user_machine_name)

        assert fetched_user.id == user_id

    def test_fetch_name_ip_machine_name_data_not_exists(self):
        """
        test fetch user by name, ip, machine_name
        check fetched user id is None
        """

        user = UserFactory()

        fetched_user = UserModel.fetch_by_name_ip_machine_name(user.name, user.ip, user.machine_name)

        assert fetched_user is None

    def test_save_data_not_exists(self, db_session):
        """
        test save user
        check saved user id, name, ip, machine_name is equal to fetched user id, name, ip, machine_name
        """

        expected_user_name = 'test_user'
        expected_user_ip = '172.16.35.10'
        expected_user_machine_name = 'test_machine'

        user = UserModel(name=expected_user_name, ip=expected_user_ip, machine_name=expected_user_machine_name)

        saved_user_id = UserModel.save(user)
        db_session.commit()
        db_session.close()

        stmt = select(UserModel).where(UserModel.name == expected_user_name
                                       and UserModel.ip == expected_user_ip
                                       and UserModel.machine_name == expected_user_machine_name)
        fetched_user = db_session.execute(stmt).scalar()

        assert saved_user_id == fetched_user.id
        assert fetched_user.name == expected_user_name
        assert fetched_user.ip == expected_user_ip
        assert fetched_user.machine_name == expected_user_machine_name

    def test_save_data_exists(self, db_session):
        """
        test save user
        check saved user id is equal to fetched user id
        """

        test_user_name = 'test_user'
        test_user_ip = '172.14.23.23'
        test_user_machine_name = 'test_machine'

        user = UserFactory(name=test_user_name, ip=test_user_ip, machine_name=test_user_machine_name)
        db_session.add(user)
        db_session.commit()
        expected_user_id = user.id
        db_session.close()

        user = UserModel(name=test_user_name, ip=test_user_ip, machine_name=test_user_machine_name)

        saved_user_id = UserModel.save(user)

        assert saved_user_id == expected_user_id
