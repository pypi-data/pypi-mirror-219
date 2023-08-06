# -*- coding: utf-8 -*-
# Copyright (2022) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""API utilities for GWDataFindServer
"""

import socket
from http import HTTPStatus
from functools import wraps

from flask import (
    current_app,
    jsonify,
    Response,
)


def error_as_json(error, code):
    """Format an error as a JSON response
    """
    return {
        "code": code,
        "title": HTTPStatus(code).phrase,
        "message": str(error),
    }


def _jsonify(out):
    if isinstance(out, tuple) and len(out) == 2:
        data, code = out
        return _jsonify(data), code
    if isinstance(out, Response):  # don't touch it
        return out
    return jsonify(out)


def as_json(func):
    """Format a function's output as a JSON reponse

    This uses :func:`flask.jsonify` to format the Response.

    If the function returns a 2-tuple, treat that as ``(data, response_code)``,
    otherwise treat the whole output as data.
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        return _jsonify(func(*args, **kwargs))
    return decorated


def _file_url(path):
    """Format a POSIX ``path`` as a ``file://`` URL

    Examples
    --------
    >>> _file_url('/data/X-TEST-0-1.gwf')
    'file://localhost/data/X-TEST-0-1.gwf'
    """
    config = current_app.config
    host = config.get('filehost', 'localhost')
    return f'file://{host}{path}'


_DEFAULT_GSIFTP_HOST = socket.gethostbyaddr(socket.gethostname())[0]
_DEFAULT_GSIFTP_PORT = 15000


def _gsiftp_url(path):
    """Format a POSIX ``path`` as a ``gsiftp://`` URL

    Examples
    --------
    >>> _gsiftp_url('/data/X-TEST-0-1.gwf')
    'gsiftp://datahost.example.com:15000/data/X-TEST-0-1.gwf'
    """
    config = current_app.config
    host = config.get('gsiftphost', _DEFAULT_GSIFTP_HOST)
    port = config.get('gsiftpport', _DEFAULT_GSIFTP_PORT)
    return f'gsiftp://{host}:{port}{path}'


def _osdf_url(path):
    """Format a POSIX ``path`` as an ``osdf://`` URL

    Examples
    --------
    >>> _osdf_url('/cvmfs/x.storage.igwn.org/data/X-TEST-0-1.gwf')
    'osdf:///data/X-TEST-0-1.gwf'
    """
    config = current_app.config
    base = None
    for section in filter(lambda x: x.startswith("osdf "), config):
        prefix = config[section].get("posix_prefix", f"/cvmfs/{section}")
        if path.startswith(prefix):
            base = config[section].get("osdf_base_path", "")
            break

    if base is None:  # nothing found, just return the original path
        return None

    return f"osdf://{path.replace(prefix, base)}"
