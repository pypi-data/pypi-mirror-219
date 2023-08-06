import shutil
from pathlib import Path


def do_cleanup():
    if (cache_path := Path("./__pb_cache__")):
        shutil.rmtree(cache_path)
