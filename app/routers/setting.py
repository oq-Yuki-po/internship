class AppRoutes:

    API_VERSION: str = "/v1.0"

    class Records:
        TAG: str = "records"
        PREFIX: str = "/records"
        POST_URL: str = "/"

    class UserSessions:
        TAG: str = "user_sessions"
        PREFIX: str = "/user_sessions"
        GET_URL: str = "/"

    class Frames:
        TAG: str = "frames"
        PREFIX: str = "/frames"
        GET_URL: str = "/{session_id}/{frame_no}"
