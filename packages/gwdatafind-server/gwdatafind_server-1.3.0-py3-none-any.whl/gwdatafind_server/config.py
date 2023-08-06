# -*- coding: utf-8 -*-
# Copyright (2019) Cardiff University
# Licensed under GPLv3+ - see LICENSE

"""Configuration manipulation for a GWDataFind Server
"""

import os.path


def get_config_path(basename='gwdatafind-server.ini'):
    """Try and locate the given basename file in a set of standard directories
    """
    # There are very few environment variables for wsgi appd we neeed
    # some absolue paths here
    ldrloc = os.getenv('LDR_LOCATION', '')
    dirs = [
        os.path.join(ldrloc, 'ldr', 'etc'),
        os.path.join(ldrloc, 'etc'),
        os.path.join(ldrloc),
        os.path.expanduser('~'),
        os.path.join(os.path.expanduser('~'), 'etc'),
        os.path.join('/', 'etc'),
    ]
    for dir_ in dirs:
        path = os.path.join(dir_, basename)
        if os.path.isfile(path):
            return path
    raise ValueError("Cannot locate {0} in any of the standard "
                     "locations: {1}".format(basename, ', '.join(dirs)))
