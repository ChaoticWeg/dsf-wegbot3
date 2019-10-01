from ..db import DatabaseHandlingCog


class MetaBaseCog(DatabaseHandlingCog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        super().__init__(bot)
