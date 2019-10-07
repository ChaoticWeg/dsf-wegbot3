from pathlib import Path
from os import path


this_dir = Path(path.realpath(path.dirname(__file__)))

ignored_cogs = ["__pycache__"]
cog_names = [f"cogs.{n.name}" for n in this_dir.iterdir() if n.is_dir() and n.name not in ignored_cogs]
