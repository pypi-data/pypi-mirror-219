# -*- coding: utf-8 -*-
# Copyright (2020) University of Wisconsin-Milwaukee
# Licensed under GPLv3+ - see LICENSE

"""Authentication for the GWDataFind Server
"""

import re
from functools import wraps

from flask import request, current_app

from jwt import InvalidTokenError
import scitokens
from scitokens.utils.errors import SciTokensException

from .api.utils import error_as_json

__author__ = 'Duncan Meacher <duncan.meacher@ligo.org>'

AUTH_METHODS = {}


def _get_auth_type():
    config = current_app.config
    authType = config['authorization']

    if authType == 'virtual_host':
        request_ip = request.environ.get(
            "SERVER_ADDR",
            request.environ.get(
                "HTTP_X_FORWARDED_HOST",
                request.remote_addr,
            ),
        )

        try:
            authType = config[request_ip]["authorization"]
        except KeyError:
            current_app.logger.info('Auth type not found,'
                                    ' using full authentication.')
            authType = "grid-mapfile,scitoken"

    if authType == "None":
        return None

    if isinstance(authType, str):
        return [x.strip() for x in authType.split(",")]

    return authType


# -- scitokens --------------

def _request_has_token(request):
    return request.headers.get("Authorization", "").startswith("Bearer")


def _get_scitokens_params():
    config = current_app.config
    audience = config['scitokens_audience']
    if isinstance(audience, str):
        audience = [audience]
    scope = config['scitokens_scope']
    issuer = config['scitokens_issuer']
    return audience, scope, issuer


def _validate_scitoken(request):
    # Get token from header
    bearer = request.headers.get("Authorization")
    auth_type, serialized_token = bearer.split()
    try:
        assert auth_type == "Bearer"
    except AssertionError:
        raise RuntimeError("Invalid header format")

    # get server params
    audience, scope, issuer = _get_scitokens_params()

    # Deserialize token
    try:
        token = scitokens.SciToken.deserialize(
            serialized_token,
            # deserialize all tokens, enforce audience later
            audience={"ANY"} | set(audience),
        )
    except (InvalidTokenError, SciTokensException) as exc:
        raise RuntimeError(f"Unable to deserialize token: {exc}")

    enforcer = scitokens.Enforcer(
        issuer,
        audience=audience,
    )

    # parse authz operation and path (if present)
    try:
        authz, path = scope.split(":", 1)
    except ValueError:
        authz = scope
        path = None

    # test the token
    if not enforcer.test(token, authz, path):
        raise RuntimeError("token enforcement failed")
    current_app.logger.info('User SciToken authorised.')


AUTH_METHODS["scitoken"] = (_request_has_token, _validate_scitoken)


# -- X.509 ------------------

def _request_has_x509(request):
    return (
        'SSL_CLIENT_S_DN' in request.headers
        and 'SSL_CLIENT_I_DN' in request.headers
    )


def _validate_x509(request):
    # Get subject and issuer from header
    subject_dn_header = request.headers.get("SSL_CLIENT_S_DN")

    # Clean up impersonation proxies. See:
    # https://git.ligo.org/lscsoft/gracedb/-/blob/master/gracedb/api/backends.py#L119
    subject_pattern = re.compile(r'^(.*?)(/CN=\d+)*$')
    subject = subject_pattern.match(subject_dn_header).group(1)

    # Check if subject is contained within grid-mapfile
    gridmap = current_app.get_gridmap_data()
    for line in gridmap:
        if subject == line:
            break
    else:
        raise RuntimeError("Subject not in grid-mapfile")
    current_app.logger.info('User X.509 proxy certificate authorised.')


AUTH_METHODS["grid-mapfile"] = (_request_has_x509, _validate_x509)


# -- handler ----------------

def _auth_error(exc):
    current_app.logger.info(f"auth error: '{exc}'")
    return error_as_json(exc, 403)


def _authorize(request):
    errors = []

    authtypes = _get_auth_type()
    if authtypes is None:
        current_app.logger.info('View request, no authentication required')
        return

    for authtype in authtypes:
        _has, _validate = AUTH_METHODS[authtype]
        if _has(request):
            try:
                _validate(request)
            except RuntimeError as exc:
                # record the error in case nothing works
                errors.append(_auth_error(exc))
                continue
            # authorized!
            return

    if not errors:
        errors.append(_auth_error("no authorization presented"))
    return errors[0]  # return the first error


def validate(func):
    @wraps(func)
    def validator(*args, **kwargs):
        errors = _authorize(request)
        if errors:
            return {"errors": errors}, 403
        return func(*args, **kwargs)

    return validator
