from pathlib import Path
from os import path


this_dir = Path(path.realpath(path.dirname(__file__)))
commands_dir = this_dir / "commands"
extensions_dir = this_dir / "extensions"

ignored_cogs = ["__pycache__"]

command_names = [f"cogs.commands.{n.name}" for n in commands_dir.iterdir() if n.is_dir() and n.name not in ignored_cogs]
ext_names = [f"cogs.extensions.{n.name}" for n in extensions_dir.iterdir() if n.is_dir() and n.name not in ignored_cogs]
cog_names = command_names + ext_names
