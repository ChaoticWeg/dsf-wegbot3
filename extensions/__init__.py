from os import path
from pathlib import Path

this_dir = Path(path.realpath(path.dirname(__file__)))
ignored = ["__pycache__"]
extension_names = [f"extensions.{c.name}" for c in this_dir.iterdir() if c.is_dir() and c.name not in ignored]
