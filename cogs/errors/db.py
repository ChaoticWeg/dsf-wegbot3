from .base import WegbotCommandError


class DatabaseNullError(WegbotCommandError):
    def __init__(self, class_name):
        super().__init__(f"database is null for cog: {class_name}")
