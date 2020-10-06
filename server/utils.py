from pathlib import Path
import secrets


def get_path(*args):
    arg = "/".join(args)
    return Path(f"/{arg}")


def prepare_workdir():
    get_path("workdir").mkdir(parents=True, exist_ok=True)


def new_tmp_dir():
    path = get_path("workdir", secrets.token_hex(32))
    path.mkdir(parents=True, exist_ok=True)
    return path
