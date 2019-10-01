from .base import WegbotCommandError


class RoleNotFoundError(WegbotCommandError):
    def __init__(self, role_name):
        super().__init__(f"no role called `{role_name}` exists in this server")


class RoleNotRequestableError(WegbotCommandError):
    def __init__(self, role_name):
        super().__init__(f"`{role_name}` cannot be requested")


class RoleAlreadyGivenError(WegbotCommandError):
    def __init__(self, role_name):
        super().__init__(f"you already have the role `{role_name}`")


class RoleNeverGivenError(WegbotCommandError):
    def __init__(self, role_name):
        super().__init__(f"you don't currently have the role `{role_name}`")
