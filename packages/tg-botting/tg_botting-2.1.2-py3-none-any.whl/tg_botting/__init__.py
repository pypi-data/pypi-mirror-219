_title__ = 'tg_botting'
__author__ = 'Sweetie'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023-present Sweetie'
__version__ = '2.1.2'

from collections import namedtuple
import logging

from .bot import Bot
from .conversions import Converter
from .message import *
from .user import *
from .utils import *
from .permissions import *
from .objects import *
from .commands import *


VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=11, micro=0, releaselevel='development', serial=0)

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
