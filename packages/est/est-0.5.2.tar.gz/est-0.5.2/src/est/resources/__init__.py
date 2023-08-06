import os
import sys
import re
import tempfile
from pathlib import Path
from typing import Optional

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources
from .generate import save_3d_exafs


def resource_path(resource: str) -> Path:
    """The resource is specified relative to the package "est.resources".
    The resource path separator can be a forward or backward slash. For example

        path = resource_path("icons/est.png")
    """
    parts = [s for s in re.split(r"[/\\]", resource) if s]
    resource = ".".join(parts[-1:])  # name and extension
    sub_package = ".".join(parts[:-1])
    if sub_package:
        package = __name__ + "." + sub_package
    else:
        package = __name__
    with resources.path(package, resource) as path:
        return path


def generate_resource(
    resource: str,
    cache: bool = True,
    overwrite: bool = False,
    output_directory: Optional[str] = None,
    word="EXAMPLE",
) -> Path:
    """Generate the derived resource from project `resource` when it does not
    exist or when `overwrite=True`. The directory in which the resource is
    located in either

    * the directory specified by argument `output_directory`
    * the user's cache directory (`cache=True`, this is the default)
    * a temporary directory (`cache=False`)
    """
    infile = resource_path(resource)
    assert infile.parent.name == "exafs"
    outname = infile.stem + ".h5"
    if output_directory:
        outdir = Path(output_directory)
    elif cache:
        outdir = get_user_resource_dir()
    else:
        outdir = Path(tempfile.gettempdir())
    outfile = outdir / outname
    if not outfile.exists() or overwrite:
        save_3d_exafs(infile, outfile, word=word)
    return outfile


def get_user_resource_dir() -> Path:
    path = get_user_cache_dir() / "resources"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_user_cache_dir() -> Path:
    home = Path().home()
    if sys.platform == "darwin":
        path = home / "Library" / "Caches"
    elif sys.platform == "win32":
        path = home / "AppData" / "Local"
        path = os.getenv("APPDATA", path)
    elif os.name == "posix":
        path = home / ".cache"
        path = os.getenv("XDG_CACHE_HOME", path)
    else:
        path = home / ".cache"

    if sys.platform == "win32":
        # On Windows cache and data dir are the same.
        # Microsoft suggest using a Cache subdirectory
        return path / "est" / "Cache"
    else:
        return path / "est"
