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
