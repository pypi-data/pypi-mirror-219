# -*- coding: utf-8 -*-
# Copyright (2022) Cardiff University
# Licensed under GPLv3+ - see LICENSE

import time

import scitokens

import pytest

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key

from gwdatafind_server import __version__ as SERVER_VERSION

from utils import create_test_app

TEST_ISSUER = "test"
TEST_AUDIENCE = "TEST"
TEST_SCOPE = "gwdatafind.read"


# -- fixtures ---------------

@pytest.fixture(scope="session")  # one per suite is fine
def private_key():
    return generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )


@pytest.fixture
def rtoken(private_key):
    """Create a token
    """
    # configure keycache
    from scitokens.utils import keycache
    kc = keycache.KeyCache.getinstance()
    kc.addkeyinfo(
        TEST_ISSUER,
        "test_key",
        private_key.public_key(),
        cache_timer=60,
    )

    # create token
    now = int(time.time())
    token = scitokens.SciToken(key=private_key, key_id="test_key")
    token.update_claims({
        "iat": now,
        "nbf": now,
        "exp": now + 86400,
        "iss": TEST_ISSUER,
        "aud": TEST_AUDIENCE,
        "scope": TEST_SCOPE,
    })
    return token


@pytest.fixture
def scitokensapp():
    return create_test_app(auth="scitoken")


@pytest.fixture
def scitokensclient(scitokensapp):
    return scitokensapp.test_client()


# -- test scitokens ---------

def _get_api_version(client, token):
    headers = {}
    if token is not None:
        serialized_token = token.serialize(issuer=TEST_ISSUER).decode("utf-8")
        headers['Authorization'] = 'Bearer {}'.format(serialized_token)
    return client.get(
        "/api/version",
        headers=headers,
    )


def test_scitokens(rtoken, scitokensclient):
    """Test that a valid token header is parsed properly
    """
    resp = _get_api_version(scitokensclient, rtoken)
    assert resp.status_code == 200, resp.json
    assert resp.json["version"] == SERVER_VERSION


def test_scitokens_failure_no_token(scitokensclient):
    """Test that a valid token header is parsed properly
    """
    resp = _get_api_version(scitokensclient, None)
    assert resp.status_code == 403, resp.json


def test_scitokens_failure_audience(rtoken, scitokensclient):
    rtoken["aud"] = "https://somethingelse.example.com"
    resp = _get_api_version(scitokensclient, rtoken)
    assert resp.status_code == 403
