from .tiktokData import *
from .instaData import *

__all__ = [name for name in globals() if not name.startswith('_')]