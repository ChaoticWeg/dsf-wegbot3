from .base import WegbotCommandError


class MetaCogError(WegbotCommandError):
    def __init__(self, message):
        super().__init__(message=message)


class RoleNotAddedError(MetaCogError):
    def __init__(self, role_name):
        super().__init__(f"it doesn't look like i registered role `{role_name}` correctly. check the logs")


class RoleAlreadyAddedError(MetaCogError):
    def __init__(self, role_name):
        super().__init__(f"it looks like `{role_name}` has already been registered")


class RoleNotRemovedError(MetaCogError):
    def __init__(self, role_name):
        super().__init__(f"it looks like role `{role_name}` was not removed. check the logs")


class RequestableRoleAsModError(MetaCogError):
    def __init__(self, role_name):
        super().__init__(f"role `{role_name}` is requestable and cannot be set as mod")
