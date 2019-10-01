from discord.ext import commands
from .. import utils

from .misc import MiscHandler
from .roles import RolesHandler
from .mods import ModsHandler


class DatabaseCog(commands.Cog, name="Database"):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self._bot = bot
        self._dbfs_root = utils.get_data_dir()

        self.roles = RolesHandler(self._dbfs_root)
        self.misc = MiscHandler(self._dbfs_root)
        self.mods = ModsHandler(self._dbfs_root)

    def initialize(self):
        self.roles.initialize()
        self.misc.initialize()
        self.mods.initialize()

    def close(self):
        print("database: closing")
        self.roles.close()
        self.misc.close()
        self.mods.close()
