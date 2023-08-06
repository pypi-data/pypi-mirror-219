# -*- coding: utf-8 -*-
# Copyright (2022) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""Test utilities for gwdatafind_server
"""

import os
from pathlib import Path
from unittest import mock

from gwdatafind_server import create_app


@mock.patch.dict("os.environ")
def create_test_app(auth=None):
    os.environ["LDR_LOCATION"] = str(Path(__file__).parent)
    app = create_app()
    if auth:  # override
        app.config["authorization"] = auth
    return app
