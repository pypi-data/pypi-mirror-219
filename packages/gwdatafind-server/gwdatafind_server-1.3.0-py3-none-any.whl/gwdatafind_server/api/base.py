# -*- coding: utf-8 -*-
# Copyright (2022) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""GWDataFind API version endpoint
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

from flask import (
    Blueprint,
    current_app,
)

from .. import (
    __version__ as VERSION,
    authentication,
)
from .utils import as_json


blueprint = Blueprint(
    "version",
    __name__,
    url_prefix="/api",
)


# -- version API

@blueprint.route("/version")
@as_json
@authentication.validate
def version():
    supported_apis = current_app.config["supported_apis"]
    return {
        "version": VERSION,
        "api_versions": supported_apis,
    }
