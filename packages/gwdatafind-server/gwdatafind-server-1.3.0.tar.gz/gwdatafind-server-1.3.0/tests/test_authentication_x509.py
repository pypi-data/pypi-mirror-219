# -*- coding: utf-8 -*-
# Copyright (2022) Cardiff University
# Licensed under GPLv3+ - see LICENSE

import pytest

from gwdatafind_server import __version__ as SERVER_VERSION

from utils import create_test_app

X509_HEADERS = {
    'SSL_CLIENT_S_DN':
        '/DC=org/DC=cilogon/C=US/O=LIGO/CN=Albert Einstein '
        'albert.einstein@ligo.org',
    'SSL_CLIENT_I_DN':
        '/DC=org/DC=cilogon/C=US/O=LIGO/CN=',
}


@pytest.fixture
def x509app():
    return create_test_app(auth="grid-mapfile")


@pytest.fixture
def x509client(x509app):
    return x509app.test_client()


def _get_api_version(client, headers=X509_HEADERS):
    return client.get(
        "/api/version",
        headers=headers,
    )


def test_x509(x509client):
    """Test that the X.509 header is parsed properly
    """
    resp = _get_api_version(x509client)
    assert resp.status_code == 200, resp.json
    assert resp.json["version"] == SERVER_VERSION


def test_x509_failure_no_header(x509client):
    """Test that not passing the X.509 header results in 403 Forbidden
    """
    resp = _get_api_version(x509client, headers=None)
    assert resp.status_code == 403, resp.json


def test_x509_failure_unauthorized(x509client):
    """Test that not passing the X.509 header results in 403 Forbidden
    """
    headers = {
        "SSL_CLIENT_S_DN": "blah blah blah",
        "SSL_CLIENT_I_DN": "blah blah blah",
    }
    resp = _get_api_version(x509client, headers=headers)
    assert resp.status_code == 403, resp.json
