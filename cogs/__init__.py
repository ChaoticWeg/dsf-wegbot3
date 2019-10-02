from os import path
from pathlib import Path

this_dir = Path(path.realpath(path.dirname(__file__)))
ignored_cogs = ["__pycache__", "errors", "utils"]
cog_names = [f"cogs.{c.name}" for c in this_dir.iterdir() if c.is_dir() and c.name not in ignored_cogs]
