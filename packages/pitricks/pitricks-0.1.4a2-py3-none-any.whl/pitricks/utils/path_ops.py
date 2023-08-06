from sys import _getframe
from pathlib import Path
import os

def pwd():
  return Path(os.path.dirname(os.path.abspath(_getframe(1).f_globals['__file__'])))