# -*- coding: utf-8 -*-
# Copyright (2022) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""Tests of `gwdatafind_server.app`
"""


def test_shutdown(app):
    """Test that `app.shutdown()` kills the cache thread
    """
    assert app.cache_manager.is_alive()
    app.shutdown()
    assert not app.cache_manager.is_alive()
