import os
from pathlib import Path

ignored_extensions = ["__init__.py"]
extension_names = [
    f"extensions.{p.name[:-3]}" for p in Path(os.path.realpath(os.path.dirname(__file__))).glob("*.py")
    if p.name not in ignored_extensions
]
