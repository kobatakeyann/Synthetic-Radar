from pathlib import Path

def generate_path(path:str) -> str:
  """generate the absolute path 

  Arg:
    path (str): synthetic_radarからの相対パス

  Return:
    str: 引数pathへの絶対パス
  """
  return str(Path(__file__).parents[2]) + path