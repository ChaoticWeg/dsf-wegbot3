from lib.errors import WegbotException


class WegbotDatabaseError(WegbotException):
    """ Base database error """
    pass


class PlatformNotSupportedError(WegbotDatabaseError):
    """ Raised when attempting to initialize the database on an unsupported platform """
    def __init__(self, platform):
        super().__init__(f"Platform not supported ({platform})")


class DatabaseNotReachableError(WegbotDatabaseError):
    """ Raised when the database cannot be reached from inside a cog or extension """
    def __init__(self, ext_name):
        super().__init__(f"Database cannot be reached from inside {ext_name}")
