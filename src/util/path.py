from pathlib import Path


def generate_path(path: str) -> str:
    """generate the absolute path

    Arg:
      path : Relative path from root directory.

    Return:
      str: Absolute path.
    """
    return str(Path(__file__).parents[2]) + path
