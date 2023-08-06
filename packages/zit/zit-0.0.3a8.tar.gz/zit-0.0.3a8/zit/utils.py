from pathlib import Path


def find_zit_root(start_path: Path):
    current_path = start_path
    while current_path != Path("/"):
        if (current_path / ".zit").is_dir():
            return current_path
        current_path = current_path.parent
    raise FileNotFoundError(
        "No .zit directory found in the current directory or any parent directories, are you inside a zit project?"
    )
