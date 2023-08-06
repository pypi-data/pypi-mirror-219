# -*- coding: utf-8 -*-
# Copyright (2022) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""Tests for `gwdatafind_server.config`
"""

import os
from pathlib import Path
from unittest import mock

import pytest

from gwdatafind_server import config


@mock.patch.dict(
    os.environ,
    {"LDR_LOCATION": str(Path(__file__).parent)},
)
def test_get_config_path():
    """Test that get_config_path() can resolve a file
    """
    assert config.get_config_path() == str(
        Path(os.environ["LDR_LOCATION"]) / "gwdatafind-server.ini"
    )


@mock.patch("os.path.isfile", return_value=False)
def test_get_config_path_error(_):
    """Test that get_config_path() errors when it can't resolve a file
    """
    with pytest.raises(ValueError):
        config.get_config_path()
