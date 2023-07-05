import datetime

from sqlalchemy import select

from app.models import FrameModel
from app.models.factories import FrameFactory, UserSessionFactory


class TestFrameModel():

    def test_fetch_by_frame_create_time_user_session_id_data_exists(self, db_session):
        """
        test fetch frame by id
        check fetched frame id is equal to saved frame id
        """

        frame = FrameFactory()
        db_session.add(frame)
        db_session.commit()
        frame_id = frame.id
        frame_create_time = frame.frame_create_time
        user_session_id = frame.user_session_id
        db_session.close()

        fetched_frame = FrameModel.fetch_by_frame_create_time_user_session_id(frame_create_time, user_session_id)
        assert fetched_frame.id == frame_id

    def test_fetch_by_frame_create_time_user_session_id_data_not_exists(self, db_session):
        """
        test fetch frame by id
        check fetched frame id is None
        """

        user_session = UserSessionFactory()
        db_session.add(user_session)
        db_session.commit()
        user_session_id = user_session.id
        db_session.close()

        frame = FrameFactory()

        fetched_frame = FrameModel.fetch_by_frame_create_time_user_session_id(frame.frame_create_time,
                                                                              user_session_id)
        assert fetched_frame is None

    def test_save_data_not_exists(self, db_session):
        """
        test save frame
        data not exists
        check saved frame id, frame_create_time, user_session_id is equal to fetched frame id, frame_create_time,
        """

        user_session = UserSessionFactory()
        db_session.add(user_session)
        db_session.commit()
        user_session_id = user_session.id
        db_session.close()

        test_frame_create_time = '2020-10-10 10:10:10'

        frame = FrameModel(frame_create_time=test_frame_create_time, user_session_id=user_session_id)
        frame_id = FrameModel.save(frame)

        db_session.commit()
        db_session.close()

        fetched_frame = db_session.execute(select(FrameModel).where(FrameModel.id == frame_id)).scalar()

        assert fetched_frame.id == frame_id
        assert fetched_frame.frame_create_time == datetime.datetime.\
            strptime(test_frame_create_time, '%Y-%m-%d %H:%M:%S').time()
        assert fetched_frame.user_session_id == user_session_id

    def test_save_data_exists(self, db_session):
        """
        test save frame
        data exists
        check saved frame id is equal to already exists in database
        """

        frame = FrameFactory()
        db_session.add(frame)
        db_session.commit()
        expected_frame_id = frame.id
        frame_create_time = frame.frame_create_time
        user_session_id = frame.user_session_id
        db_session.close()

        test_frame = FrameModel(frame_create_time=frame_create_time, user_session_id=user_session_id)
        frame_id = FrameModel.save(test_frame)

        assert frame_id == expected_frame_id
