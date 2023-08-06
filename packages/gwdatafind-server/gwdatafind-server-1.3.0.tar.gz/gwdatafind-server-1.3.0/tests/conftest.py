# -*- coding: utf-8 -*-
# Copyright (2019) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""Test configuration for gwdatafind_server
"""

import pytest

from utils import create_test_app


@pytest.fixture
def app():
    # default app to noauth for ease
    return create_test_app(auth="None")


@pytest.fixture
def client(app):
    return app.test_client()
