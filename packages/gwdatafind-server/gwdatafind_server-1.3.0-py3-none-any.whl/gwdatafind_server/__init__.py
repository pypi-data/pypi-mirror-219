# -*- coding: utf-8 -*-
# Copyright (2019) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""The GWDataFind Service provides a metadata-based
data discover mechanism for data files.

Users provide a few key details as part of an HTTP(S)
query and receive URLs that indicate the locations
of the relevant data.
"""

try:
    from ._version import version as __version__
except ModuleNotFoundError:  # development mode
    __version__ = 'dev'

from .app import GWDataFindApp
from .config import get_config_path


def create_app():
    """Create an instance of the application
    """
    return GWDataFindApp(__name__, get_config_path())
