from pathlib import Path
from os import path

this_dir = Path(path.realpath(path.dirname(__file__)))
commands_dir = this_dir / "commands"
extensions_dir = this_dir / "extensions"

ignored_cogs = ["__pycache__", "__init__.py"]


command_dirs = [f"cogs.commands.{n.name}"
                for n in commands_dir.iterdir()
                if n.is_dir()
                and n.name not in ignored_cogs]

command_files = [f"cogs.commands.{n.name[:-3]}"
                 for n in commands_dir.iterdir()
                 if n.is_file()
                 and n.name not in ignored_cogs]

ext_dirs = [f"cogs.extensions.{n.name}"
            for n in extensions_dir.iterdir()
            if n.is_dir()
            and n.name not in ignored_cogs]

ext_files = [f"cogs.extensions.{n.name[:-3]}"
             for n in extensions_dir.iterdir()
             if n.is_file()
             and n.name not in ignored_cogs]

cog_names = command_dirs + command_files + ext_dirs + ext_files
